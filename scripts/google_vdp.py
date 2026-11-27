"""Fetch and deliver Digital Lab VDPs through Google APIs."""

import argparse
from contextlib import contextmanager
from datetime import date, datetime
import hashlib
import json
from math import isclose
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import NamedTemporaryFile
from urllib.parse import parse_qs, urlsplit
from zipfile import ZipFile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google_workspace import (
    DRIVE, PRIVATE, ROOT, SHEETS, UPLOAD, GoogleError, TransportError,
    WorkspaceError, authorize, connect, desktop_client,
)


PPTX = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
FOLDER = 'application/vnd.google-apps.folder'
SLIDES = 'application/vnd.google-apps.presentation'
FILE_FIELDS = 'id,name,mimeType,parents,driveId,capabilities,md5Checksum,size,webViewLink,trashed,createdTime'
VDP = re.compile(r'P\d+_MATHS_N([1-3])_SEM(\d+)_VDP\d+', re.IGNORECASE)
GOOGLE_ID = re.compile(r'[A-Za-z0-9_-]+')
CHUNK = 8 * 1024 * 1024


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def read_settings():
    references = PRIVATE / 'google-references'
    if not references.is_dir():
        references = Path.home() / '.codex/skills/digital-lab-project/private'
    try:
        tracker = read_json(references / 'storyboard-tracker.json')
        folder = read_json(references / 'video-delivery-folder.json')
    except FileNotFoundError:
        raise WorkspaceError('Missing Google tracker and delivery folder references. See docs/google-vdp.md.') from None
    sheet_url = urlsplit(tracker['url'])
    spreadsheet = re.fullmatch(r'/spreadsheets/d/([\w-]+)/edit/?', sheet_url.path)
    if sheet_url.hostname != 'docs.google.com' or not spreadsheet:
        raise WorkspaceError('The tracker reference must be a Google Sheets edit link')
    url_args = parse_qs(sheet_url.fragment) | parse_qs(sheet_url.query)
    if tracker['account'].casefold() != folder['account'].casefold():
        raise WorkspaceError('Tracker and Drive references specify different Google accounts')
    return spreadsheet[1], url_args.get('gid', [''])[0], file_reference(folder['url']), tracker['account']


def file_reference(url):
    parsed = urlsplit(url)
    params = parse_qs(parsed.query)
    if parsed.scheme == 'https' and parsed.hostname in ('drive.google.com', 'docs.google.com'):
        path_id = re.search(r'/(?:d|folders)/([\w-]+)(?:/|$)', parsed.path)
        file_id = path_id[1] if path_id else params.get('id', [''])[0]
        key = params.get('resourcekey', [''])[0]
        if GOOGLE_ID.fullmatch(file_id) and (not key or GOOGLE_ID.fullmatch(key)):
            return file_id, key
    raise WorkspaceError('Expected a Google Drive file or folder link')


def file_headers(reference):
    file_id, key = reference
    return {'X-Goog-Drive-Resource-Keys': f'{file_id}/{key}'} if key else {}


def drive_file(api, reference):
    return api.json('Read Drive file', DRIVE + '/files/' + reference[0],
                    query={'fields': FILE_FIELDS, 'supportsAllDrives': 'true'},
                    headers=file_headers(reference))


def child_folder(api, parent, name):
    query = {
        'q': f"'{parent['id']}' in parents and trashed = false and mimeType = '{FOLDER}' and name = '{name}'",
        'fields': f'nextPageToken,files({FILE_FIELDS})',
        'supportsAllDrives': 'true',
        'includeItemsFromAllDrives': 'true',
    }
    if parent.get('driveId'):
        query.update(corpora='drive', driveId=parent['driveId'])
    matches = []
    while True:
        result = api.json('Find delivery folder', DRIVE + '/files', query=query)
        matches.extend(result.get('files', []))
        if not result.get('nextPageToken'):
            break
        query['pageToken'] = result['nextPageToken']
    if len(matches) != 1:
        raise WorkspaceError(f'Expected one Drive folder named {name!r}. Found {len(matches)}.')
    return matches[0]


def column_index(column):
    number = 0
    for char in column:
        number = number * 26 + ord(char) - ord('A') + 1
    return number - 1


def column_label(index):
    label = ''
    while index >= 0:
        index, digit = divmod(index, 26)
        label = chr(ord('A') + digit) + label
        index -= 1
    return label


def a1(title, cells):
    return "'" + title.replace("'", "''") + "'!" + cells


def cell_link(cell):
    links = {run.get('format', {}).get('link', {}).get('uri') for run in cell.get('textFormatRuns', [])}
    links.update(run.get('chip', {}).get('richLinkProperties', {}).get('uri') for run in cell.get('chipRuns', []))
    links.discard(None)
    direct = cell.get('hyperlink')
    if direct:
        links.add(direct)
    value = cell.get('userEnteredValue', {}).get('stringValue', '') or cell.get('formattedValue', '')
    if value.startswith('https://'):
        links.add(value)
    if len(links) > 1:
        raise WorkspaceError('A tracker cell contains several distinct links')
    return next(iter(links), '')


def cell_at(row, column):
    values = row.get('values', [])
    return values[column] if column < len(values) else {}


CELL_FIELDS = ('userEnteredValue,formattedValue,hyperlink,textFormatRuns(format(link)),'
               'chipRuns(chip(richLinkProperties(uri)))')


def sheet_rows(api, spreadsheet, cell_range):
    result = api.json('Read tracker cells', f'{SHEETS}/{spreadsheet}', query={
        'ranges': cell_range,
        'fields': f'sheets(data(rowData(values({CELL_FIELDS}))))',
    })
    return (result['sheets'][0].get('data') or [{}])[0].get('rowData', [])


def resolve(api, spreadsheet, gid, cell, version):
    match = re.fullmatch(r'([A-Z]{1,3})([1-9][0-9]*)', cell.upper())
    if not match or not gid.isdecimal():
        raise WorkspaceError('Supply a storyboard cell such as F8 and a numeric Google Sheets gid')
    column, row = column_index(match[1]), int(match[2])
    meta = api.json('Read tracker tabs', f'{SHEETS}/{spreadsheet}', query={
        'fields': 'properties(timeZone),sheets(properties(sheetId,title,gridProperties(columnCount,rowCount)))',
    })
    tabs = [item['properties'] for item in meta['sheets'] if item['properties']['sheetId'] == int(gid)]
    if not tabs:
        raise WorkspaceError('The requested sheet tab was not found')
    tab = tabs[0]
    title = tab['title']
    grid = tab['gridProperties']
    if row > grid['rowCount'] or column >= grid['columnCount']:
        raise WorkspaceError('The storyboard cell is outside the selected tab')
    rows = sheet_rows(api, spreadsheet, a1(title, f'A1:{column_label(grid["columnCount"] - 1)}{row}'))
    if len(rows) < row:
        raise WorkspaceError('The storyboard cell is empty')

    accepted_headers = {f'version {version}'}
    if version == 1:
        accepted_headers.add('video1')
    headers = [entry for entry in rows[:row - 1]
               if cell_at(entry, column).get('formattedValue', '').strip().casefold() == 'storyboard']
    columns = [i for i, value in enumerate(headers[-1]['values'])
               if ' '.join(value.get('formattedValue', '').split()).casefold() in accepted_headers] if headers else []
    if len(columns) != 1:
        raise WorkspaceError(f'Expected one Version {version} header beside the Storyboard column')
    labels = [entry.get('formattedValue', '').strip().casefold() for entry in headers[-1]['values']]
    date_column = next((i for i in range(columns[0] + 1, len(labels) - 1)
                        if labels[i:i + 2] == ['date', 'heure']), None) if version == 1 else None
    source_link = cell_link(cell_at(rows[row - 1], column))
    if not source_link:
        raise WorkspaceError('The storyboard cell has no Drive link')
    source_ref = file_reference(source_link)
    source = drive_file(api, source_ref)
    name = source['name'].strip()
    identity = VDP.match(name)
    if source.get('trashed') or source['mimeType'] not in (PPTX, SLIDES) or not identity:
        raise WorkspaceError('The linked Drive file is not a Digital Lab VDP storyboard')
    level, week = int(identity[1]), int(identity[2])
    if week < 1:
        raise WorkspaceError('Invalid week in the VDP identifier')
    tab_week = re.search(r'\bsemaine\s+(\d+)\b', title, re.IGNORECASE)
    if tab_week and int(tab_week[1]) != week:
        raise WorkspaceError('The VDP identifier and sheet tab refer to different weeks')
    return {
        'title': title, 'sourceCell': cell.upper(), 'sourceRef': source_ref, 'source': source,
        'versionCell': f'{column_label(columns[0])}{row}', 'version': version,
        'deliveryDateColumn': date_column, 'trackerTimeZone': meta.get('properties', {}).get('timeZone'),
        'lesson': identity[0].upper(), 'level': f'{level}AC', 'week': week,
    }


def fetch_storyboard(api, job, output):
    source_key = job['sourceRef']
    query = {'alt': 'media', 'supportsAllDrives': 'true'}
    route = '/files/' + source_key[0]
    if job['source']['mimeType'] == SLIDES:
        route += '/export'
        query = {'mimeType': PPTX}
    output = output or ROOT / 'outputs/google-vdp/storyboards' / f'{job["lesson"]}.pptx'
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, suffix='.part', delete=False) as temp:
        temp_path = Path(temp.name)
        try:
            with api.open('Download storyboard', DRIVE + route, query=query, headers=file_headers(source_key)) as response:
                shutil.copyfileobj(response, temp)
            temp.close()
            with ZipFile(temp_path) as deck:
                if 'ppt/presentation.xml' not in deck.namelist() or deck.testzip() is not None:
                    raise WorkspaceError('The downloaded file is not a valid PowerPoint storyboard')
            if output.is_file():
                with output.open('rb') as existing, temp_path.open('rb') as downloaded:
                    if hashlib.file_digest(existing, 'sha256').digest() == hashlib.file_digest(downloaded, 'sha256').digest():
                        return output
                raise WorkspaceError('A different local storyboard already exists at the requested path')
            temp_path.rename(output)
            return output
        finally:
            temp.close()
            temp_path.unlink(missing_ok=True)


def destination(api, folder_ref, job):
    root = drive_file(api, folder_ref)
    if root['mimeType'] != FOLDER or root.get('trashed'):
        raise WorkspaceError('The configured delivery link does not point to an active Drive folder')
    return child_folder(api, child_folder(api, root, job['level']), f'Semaine {job["week"]}')


def review_video(video, job):
    version = job['version']
    lesson = job['lesson']
    accepted = {f'{lesson}_V{version}.mp4'}
    if version == 1:
        accepted.add(f'{lesson}.mp4')
    if video.name.upper() not in {name.upper() for name in accepted} or not video.is_file():
        raise WorkspaceError('The MP4 filename must match the VDP identifier and delivery version')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(video)],
                           capture_output=True, check=False)
    if probe.returncode:
        raise WorkspaceError('FFprobe could not read the proposed MP4')
    streams = json.loads(probe.stdout)['streams']
    if not any((stream.get('codec_name'), stream.get('width'), stream.get('height'), stream.get('r_frame_rate'))
               == ('h264', 1920, 1080, '30/1') for stream in streams):
        raise WorkspaceError('Delivery requires a 1920×1080 H.264 stream at 30 fps')
    if not any(stream.get('codec_name') == 'aac' for stream in streams):
        raise WorkspaceError('Delivery requires an AAC audio stream')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(video),
                    '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], check=True)


def save_job(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2), encoding='utf-8')
    temp.replace(path)


@contextmanager
def lock_job(path):
    import msvcrt

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix('.lock').open('a+b') as lock:
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise WorkspaceError('Another process is delivering this VDP version') from None
        yield


def start_upload(api, state, video, folder_id):
    reference = state.get('replace')
    url = f'{UPLOAD}/{reference[0]}' if reference else UPLOAD
    metadata = {'name': video.name}
    if not reference:
        metadata.update(id=state['id'], mimeType='video/mp4', parents=[folder_id])
    headers = {'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(state['size'])}
    if reference:
        headers.update(file_headers(reference))
    with api.open('Start resumable MP4 upload', url, method='PATCH' if reference else 'POST', query={
        'uploadType': 'resumable', 'supportsAllDrives': 'true', 'fields': FILE_FIELDS,
    }, headers=headers, body=metadata) as response:
        url = response.headers.get('Location', '')
    validate_upload_url(url, reference)
    return url


def validate_upload_url(url, reference=None):
    parsed = urlsplit(url)
    path = urlsplit(UPLOAD).path
    paths = (path, f'{path}/{reference[0]}') if reference else (path,)
    if parsed.scheme != 'https' or parsed.netloc != 'www.googleapis.com' or parsed.path not in paths:
        raise WorkspaceError('Google returned an unexpected resumable upload endpoint')


def upload(api, state, state_path, video, folder):
    size = state['size']
    with video.open('rb') as content:
        failures = 0
        position = 0
        check_position = bool(state.get('session'))
        while failures < 5:
            try:
                if not state.get('session'):
                    state['session'] = start_upload(api, state, video, folder)
                    save_job(state_path, state)
                    position = 0
                session = state['session']
                validate_upload_url(session, state.get('replace'))
                if check_position:
                    payload, span = b'', f'bytes */{size}'
                else:
                    content.seek(position)
                    payload = content.read(min(CHUNK, size - position))
                    if not payload:
                        raise WorkspaceError('The local MP4 changed during upload')
                    span = f'bytes {position}-{position + len(payload) - 1}/{size}'
                with api.open('Upload MP4 bytes', session, method='PUT', body=payload,
                              headers={'Content-Range': span, 'Content-Type': 'video/mp4'},
                              allowed=(308, 404)) as response:
                    if response.status in (200, 201):
                        return
                    if response.status == 404:
                        state.pop('session', None)
                        save_job(state_path, state)
                        failures += 1
                        check_position = False
                        continue
                    received = response.headers.get('Range', '')
                    end = re.fullmatch(r'bytes=0-(\d+)', received) if received else None
                    next_position = int(end[1]) + 1 if end else 0
                    if (received and not end) or next_position >= size:
                        raise WorkspaceError('Drive returned an invalid upload offset')
                    failures = 0 if next_position > position else failures + (not check_position)
                    position, check_position = next_position, False
            except (GoogleError, TransportError) as error:
                if isinstance(error, GoogleError) and error.status == 409:
                    return
                if isinstance(error, GoogleError) and error.status not in (408, 429, 500, 502, 503, 504):
                    raise
                check_position = True
                failures += 1
    raise WorkspaceError('MP4 upload interrupted. Rerun the same delivery to resume.')


def version_cell(api, spreadsheet, job):
    target = a1(job['title'], job['versionCell'])
    rows = sheet_rows(api, spreadsheet, target)
    return rows[0]['values'][0] if rows and rows[0].get('values') else {}


def matches_video(file, folder, checksum, size, name):
    return (not file.get('trashed') and file.get('md5Checksum') == checksum
            and file.get('size') == str(size) and file.get('mimeType') == 'video/mp4'
            and folder in file.get('parents', []) and file.get('name', '').casefold() == name.casefold())


def video_fingerprint(video):
    with video.open('rb') as content:
        return video.stat().st_size, hashlib.file_digest(content, 'md5').hexdigest()


def deliver(api, spreadsheet, gid, job, folder, video):
    if job['version'] != 1:
        raise WorkspaceError('Use revise with the existing video link for a revised delivery')
    folder_id = folder['id']
    size, checksum = video_fingerprint(video)
    state_key = '\n'.join((spreadsheet, gid, job['lesson'], str(job['version'])))
    state_path = PRIVATE / 'google-deliveries' / (hashlib.sha256(state_key.encode()).hexdigest() + '.json')
    with lock_job(state_path):
        return publish(api, spreadsheet, job, folder_id, video, size, checksum, state_path)


def publish(api, spreadsheet, job, folder, video, size, checksum, state_path):
    cell = version_cell(api, spreadsheet, job)
    existing = cell_link(cell)
    if existing:
        reference = file_reference(existing)
        file = drive_file(api, reference)
        if matches_video(file, folder, checksum, size, video.name):
            return finish_first_delivery(api, spreadsheet, job, existing, file)
    if cell.get('userEnteredValue') or cell.get('formattedValue') or existing:
        raise WorkspaceError(f'{job["versionCell"]} already contains a different value')

    expected = {'size': size, 'md5': checksum, 'folder': folder, 'name': video.name}
    if state_path.exists():
        state = read_json(state_path)
        if any(state.get(key) != value for key, value in expected.items()):
            raise WorkspaceError('This VDP version already has a delivery receipt for another MP4 or folder')
    else:
        result = api.json('Reserve Drive file ID', DRIVE + '/files/generateIds', query={'count': 1, 'space': 'drive'})
        state = {**expected, 'id': result['ids'][0]}
        save_job(state_path, state)
    try:
        file = drive_file(api, (state['id'], ''))
    except GoogleError as error:
        if error.status != 404:
            raise
        upload(api, state, state_path, video, folder)
        file = drive_file(api, (state['id'], ''))
    if not matches_video(file, folder, checksum, size, video.name):
        raise WorkspaceError('Drive did not return the expected MP4 bytes and folder')
    state.pop('session', None)
    save_job(state_path, state)
    link = file.get('webViewLink') or f'https://drive.google.com/file/d/{file["id"]}/view'
    reference = file_reference(link)
    if reference[0] != state['id']:
        raise WorkspaceError('Drive returned a link to a different file')
    # Revalidate the workbook mapping after the potentially long upload.
    refreshed = resolve(api, spreadsheet, str(job['gid']), job['sourceCell'], job['version'])
    if any(refreshed[key] != job[key] for key in ('title', 'sourceRef', 'versionCell', 'lesson')):
        raise WorkspaceError('The VDP row or destination changed during upload')
    return finish_first_delivery(api, spreadsheet, {**refreshed, 'gid': job['gid']}, link, file)


def finish_first_delivery(api, spreadsheet, job, link, file):
    chip = publish_video_chip(api, spreadsheet, job, link)
    record_first_delivery(api, spreadsheet, job, file.get('createdTime'))
    return chip


def record_first_delivery(api, spreadsheet, job, created_time):
    column = job['deliveryDateColumn']
    if column is None:
        return
    row = int(re.search(r'\d+$', job['versionCell'])[0])
    target = a1(job['title'], f'{column_label(column)}{row}:{column_label(column + 1)}{row}')
    records = sheet_rows(api, spreadsheet, target)
    cells = records[0] if records else {}
    missing = [offset for offset in range(2)
               if not any(cell_at(cells, offset).get(key) for key in ('userEnteredValue', 'formattedValue'))]
    if not missing:
        return
    if not created_time or not job['trackerTimeZone']:
        raise WorkspaceError('The upload time or tracker time zone is missing')
    try:
        local = datetime.fromisoformat(created_time).astimezone(ZoneInfo(job['trackerTimeZone']))
    except (ValueError, ZoneInfoNotFoundError) as error:
        raise WorkspaceError(f'Cannot convert the upload time to the tracker time zone: {error}') from error
    values = [(local.date() - date(1899, 12, 30)).days, (local.hour * 60 + local.minute) / 1440]
    formats = [{'type': 'DATE', 'pattern': 'd/m/yyyy'}, {'type': 'TIME', 'pattern': 'hh:mm'}]
    requests = [{'updateCells': {
        'start': {'sheetId': int(job['gid']), 'rowIndex': row - 1, 'columnIndex': column + offset},
        'rows': [{'values': [{
            'userEnteredValue': {'numberValue': values[offset]},
            'userEnteredFormat': {'numberFormat': formats[offset]},
        }]}],
        'fields': 'userEnteredValue,userEnteredFormat.numberFormat',
    }} for offset in missing]
    api.json('Write original MP4 delivery date and time', f'{SHEETS}/{spreadsheet}:batchUpdate',
             method='POST', body={'requests': requests})
    written = sheet_rows(api, spreadsheet, target)
    if not written or any(not isclose(cell_at(written[0], i).get('userEnteredValue', {}).get('numberValue', float('nan')),
                                      values[i], rel_tol=0, abs_tol=1e-10) for i in missing):
        raise WorkspaceError('The delivery date and time could not be confirmed')


def has_public_link(api, reference):
    route = DRIVE + '/files/' + reference[0] + '/permissions'
    query = {'supportsAllDrives': 'true', 'pageSize': 100,
             'fields': 'nextPageToken,permissions(type,role,view)'}
    while True:
        result = api.json('Check public Drive link', route, query=query, headers=file_headers(reference))
        if any(permission.get('type') == 'anyone'
               and permission.get('role') in ('reader', 'commenter', 'writer')
               and not permission.get('view')
               for permission in result.get('permissions', [])):
            return True
        token = result.get('nextPageToken')
        if not token:
            return False
        query['pageToken'] = token


def ensure_public_link(api, reference):
    file_id = reference[0]
    lock = PRIVATE / 'google-deliveries' / f'{file_id}-public.lock'
    with lock_job(lock):
        if has_public_link(api, reference):
            return
        api.json('Share MP4 with anyone who has the link', DRIVE + '/files/' + file_id + '/permissions',
                 method='POST', query={'supportsAllDrives': 'true'}, headers=file_headers(reference),
                 body={'type': 'anyone', 'role': 'reader', 'allowFileDiscovery': False})
        if not has_public_link(api, reference):
            raise WorkspaceError('Drive did not confirm public read access to the MP4')


def video_chip_link(cell):
    # Sheets resolves the write placeholder to the filename in its read response.
    chips = cell.get('chipRuns', [])
    if len(chips) != 1 or chips[0].get('startIndex', 0) != 0:
        return ''
    return chips[0].get('chip', {}).get('richLinkProperties', {}).get('uri', '')


def publish_video_chip(api, spreadsheet, job, link):
    reference = file_reference(link)
    ensure_public_link(api, reference)
    current = version_cell(api, spreadsheet, job)
    existing = cell_link(current)
    if existing:
        existing_reference = file_reference(existing)
        if existing_reference[0] != reference[0]:
            raise WorkspaceError(f'{job["versionCell"]} contains a different Drive file')
        if video_chip_link(current):
            return video_chip_link(current)
        # Preserve the existing resource key when converting a plain link.
        link = existing if existing_reference[1] or not reference[1] else link
    elif current.get('userEnteredValue') or current.get('formattedValue'):
        raise WorkspaceError(f'{job["versionCell"]} was filled during delivery')

    column, row = re.fullmatch(r'([A-Z]+)([0-9]+)', job['versionCell']).groups()
    update = {
        'start': {'sheetId': int(job['gid']), 'rowIndex': int(row) - 1, 'columnIndex': column_index(column)},
        'rows': [{'values': [{
            'userEnteredValue': {'stringValue': '@'},
            'chipRuns': [{'startIndex': 0, 'chip': {'richLinkProperties': {'uri': link}}}],
        }]}],
        'fields': 'userEnteredValue,chipRuns',
    }
    api.json('Write MP4 file chip to tracker', f'{SHEETS}/{spreadsheet}:batchUpdate',
             method='POST', body={'requests': [{'updateCells': update}]})
    applied = video_chip_link(version_cell(api, spreadsheet, job))
    if not applied or file_reference(applied) != file_reference(link):
        raise WorkspaceError('The tracker video chip could not be confirmed')
    return applied


def verify_delivery(api, spreadsheet, job, folder, video):
    cell = version_cell(api, spreadsheet, job)
    link = cell_link(cell)
    if not link:
        raise WorkspaceError('The selected version cell does not contain a Drive link')
    reference = file_reference(link)
    file = drive_file(api, reference)
    size, checksum = video_fingerprint(video)
    if not matches_video(file, folder['id'], checksum, size, video.name):
        raise WorkspaceError('The linked MP4 differs from the local export or expected folder')
    if not has_public_link(api, reference):
        raise WorkspaceError('The linked MP4 is restricted on Drive')
    chip = video_chip_link(cell)
    if not chip or file_reference(chip) != reference:
        raise WorkspaceError('The tracker cell does not contain a Drive video chip')
    return chip


def revise(api, spreadsheet, job, version, folder, video):
    size, checksum = video_fingerprint(video)
    # Serialize revisions to the same Drive file even when invoked from a different linked cell.
    link = cell_link(version_cell(api, spreadsheet, job))
    if not link:
        raise WorkspaceError('The selected version cell must contain the existing Drive link')
    reference = file_reference(link)
    file_id = reference[0]
    folder_id = folder['id']
    state_dir = PRIVATE / 'google-deliveries'
    lock_path = state_dir / (hashlib.sha256(file_id.encode()).hexdigest() + '.json')
    with lock_job(lock_path):
        if cell_link(version_cell(api, spreadsheet, job)) != link:
            raise WorkspaceError('The selected Drive link changed before revision')
        current = drive_file(api, reference)
        if matches_video(current, folder_id, checksum, size, video.name):
            return publish_video_chip(api, spreadsheet, job, link)
        prior_name = re.fullmatch(rf'{re.escape(job["lesson"])}(?:_V(\d+))?\.mp4',
                                  current.get('name', ''), re.IGNORECASE)
        if (not prior_name or current.get('trashed') or folder_id not in current.get('parents', [])
                or current.get('mimeType') != 'video/mp4'):
            raise WorkspaceError('The linked file is not this VDP in the expected delivery folder')
        if int(prior_name[1] or 1) >= version or not current.get('capabilities', {}).get('canModifyContent'):
            raise WorkspaceError('The linked file needs an older version number and content-edit access')
        expected = {'id': file_id, 'replace': list(reference), 'size': size, 'md5': checksum,
                    'folder': folder_id, 'name': video.name, 'priorMd5': current.get('md5Checksum')}
        state_path = lock_path.with_name(lock_path.stem + f'-v{version}.json')
        state = read_json(state_path) if state_path.exists() else expected.copy()
        if any(state.get(key) != value for key, value in expected.items()):
            raise WorkspaceError('The pending revision targets different video bytes or a changed Drive file')
        upload(api, state, state_path, video, folder_id)
        if not matches_video(drive_file(api, reference), folder_id, checksum, size, video.name):
            raise WorkspaceError('Drive did not return the expected revised video bytes')
        state.pop('session', None)
        save_job(state_path, state)
        if cell_link(version_cell(api, spreadsheet, job)) != link:
            raise WorkspaceError('The Drive file was revised, but the link in Sheets changed during the upload')
        return publish_video_chip(api, spreadsheet, job, link)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action', required=True)
    actions.add_parser('auth', help='authorize your own Google Workspace account')
    for name in ('inspect', 'fetch', 'verify', 'deliver', 'revise'):
        command = actions.add_parser(name)
        command.add_argument('--gid', help='Google Sheets tab ID, defaults to the saved tracker tab')
        command.add_argument('--cell', required=True, help='source Storyboard cell, for example F8')
        command.add_argument('--version', type=int, default=1)
        if name == 'fetch':
            command.add_argument('--output', type=Path)
        if name in ('verify', 'deliver', 'revise'):
            command.add_argument('--mp4', required=True, type=Path)
        if name in ('verify', 'revise'):
            command.add_argument('--link-version', required=name == 'revise', type=int,
                                 help='the existing Version N column that contains the stable Drive link')
    args = parser.parse_args()
    try:
        spreadsheet, default_gid, folder_ref, account = read_settings()
        client = desktop_client(PRIVATE / 'google-oauth-client.json')
        token_path = PRIVATE / 'google-workspace-token.dpapi'
        if args.action == 'auth':
            authorize(client, account, token_path)
            print('Connected the work account. Future operations use the Google APIs.')
            return 0
        link_version = getattr(args, 'link_version', None)
        if link_version is None:
            link_version = args.version
        if args.version < 1 or not 1 <= link_version <= args.version:
            parser.error('Select a positive version and an existing link column no later than that version')
        if args.action == 'deliver' and args.version != 1:
            parser.error('Use revise with the existing video link for a revised delivery')
        gid = args.gid or default_gid
        api = connect(client, account, token_path)
        job = resolve(api, spreadsheet, gid, args.cell, link_version)
        job['gid'] = gid
        if args.action == 'fetch':
            print(fetch_storyboard(api, job, args.output))
            return 0
        folder = destination(api, folder_ref, job)
        if args.action == 'inspect':
            current = version_cell(api, spreadsheet, job)
            print(json.dumps({
                'lesson': job['lesson'], 'tab': job['title'], 'storyboard': job['sourceCell'],
                'versionCell': job['versionCell'], 'existingLink': bool(cell_link(current)),
                'occupied': bool(current.get('userEnteredValue') or current.get('formattedValue') or cell_link(current)),
                'folder': f'{job["level"]}/Semaine {job["week"]}',
                'canAddChildren': folder.get('capabilities', {}).get('canAddChildren', False),
            }, ensure_ascii=False))
            return 0
        review_video(args.mp4, {**job, 'version': args.version})
        if args.action == 'revise':
            print(revise(api, spreadsheet, job, args.version, folder, args.mp4))
        elif args.action == 'verify':
            print(verify_delivery(api, spreadsheet, job, folder, args.mp4))
        else:
            print(deliver(api, spreadsheet, gid, job, folder, args.mp4))
        return 0
    except (WorkspaceError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Digital Lab: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
