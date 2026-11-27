"""Read Digital Lab's weekly tracker and detect newly linked storyboards."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import re
import sys
from zoneinfo import ZoneInfo

import google_vdp as delivery
from google_workspace import GoogleError, WorkspaceError, connect, desktop_client


STATE = delivery.PRIVATE / 'storyboard-watch' / 'all-weeks.json'
WEEK_TAB = re.compile(r'\bsemaine\s+\d+\b', re.IGNORECASE)
STORYBOARD_FORMATS = {delivery.PPTX, delivery.SLIDES}
REPORT_TIME_ZONE = 'Africa/Casablanca'
IN_PRODUCTION = re.compile(
    r'^(?:en\s+cours\b|(?:en\s+)?(?:corrections?|rectifs?|rectifications?)$|[àa]\s+(?:corriger|rectifier)$)',
    re.IGNORECASE,
)


def value(row, column):
    return delivery.cell_at(row, column).get('formattedValue', '').strip()


def local_time(timestamp):
    if not timestamp:
        return None
    return datetime.fromisoformat(timestamp.replace('Z', '+00:00')).astimezone(
        ZoneInfo(REPORT_TIME_ZONE)).strftime('%d/%m/%Y %H:%M')


def observe(active, state, checked_at, baseline=False):
    """Record actual detection time, without inventing dates for legacy seen keys."""
    seen = set(state.get('seen', []))
    first = dict(state.get('firstDetectedAt', {}))
    observed = []
    new = []
    for row in active:
        if row['key'] not in seen:
            first.setdefault(row['key'], checked_at)
        entry = {**row, 'firstDetectedAt': first.get(row['key']),
                 'firstDetectedLocal': local_time(first.get(row['key'])),
                 'driveCreatedLocal': local_time(row.get('driveCreatedAt'))}
        observed.append(entry)
        if row['key'] not in seen and not baseline:
            new.append(entry)
    updated = {**state, 'seen': sorted(seen | {row['key'] for row in active}),
               'firstDetectedAt': first}
    return observed, new, updated


def scan(api, book):
    meta = api.json('Find weekly tracker tabs', f'{delivery.SHEETS}/{book}', query={
        'fields': 'sheets(properties(sheetId,title))',
    })
    tabs = [sheet['properties'] for sheet in meta['sheets']
            if WEEK_TAB.search(sheet['properties']['title'])]
    if not tabs:
        raise WorkspaceError('No weekly tabs found in the Digital Lab tracker')
    data = api.json('Read weekly storyboard and video links', f'{delivery.SHEETS}/{book}', query={
        'ranges': [delivery.a1(tab['title'], 'A:M') for tab in tabs],
        'fields': f'sheets(properties(sheetId,title),data(startRow,rowData(values({delivery.CELL_FIELDS}))))',
    })
    candidates = []
    invalid = []
    for tab in data.get('sheets', []):
        props = tab['properties']
        for block in tab.get('data', []):
            for n, row in enumerate(block.get('rowData', []), block.get('startRow', 0) + 1):
                cell = delivery.cell_at(row, 5)
                link = delivery.cell_link(cell)
                if not link:
                    continue
                candidate = {
                    'week': props['title'].strip(), 'gid': props['sheetId'], 'cell': f'F{n}',
                    'level': value(row, 0), 'lesson': value(row, 4), 'typeLabel': value(row, 1),
                    'status': value(row, 9), 'motionDesigner': value(row, 8), 'link': link,
                    'videoLinked': any(delivery.cell_link(delivery.cell_at(row, i)) for i in (10, 11, 12)),
                }
                try:
                    candidate['ref'] = delivery.file_reference(link)
                except WorkspaceError:
                    invalid.append({**candidate, 'reason': 'Lien hors de Google Drive'})
                    continue
                candidates.append(candidate)

    refs = list(dict.fromkeys(row['ref'] for row in candidates))

    def get_file(ref):
        try:
            return api.json('Verify linked storyboard in Drive', f'{delivery.DRIVE}/files/{ref[0]}',
                            query={'supportsAllDrives': 'true', 'fields': 'name,mimeType,trashed,createdTime'},
                            headers=delivery.file_headers(ref))
        except GoogleError as error:
            if error.status not in (403, 404, 410):
                raise
            return {'error': str(error)}

    with ThreadPoolExecutor(max_workers=4) as pool:
        files = dict(zip(refs, pool.map(get_file, refs)))

    active = []
    for row in candidates:
        ref = row.pop('ref')
        file = files[ref]
        if file.get('error') or file.get('trashed') or file.get('mimeType') not in STORYBOARD_FORMATS:
            invalid.append({**row, 'reason': file.get('error') or ('Corbeille' if file.get('trashed') else 'Format du lien')})
            continue
        suffix = re.search(r'_(VDP|VM)\d+', file['name'], re.IGNORECASE)
        kind = (suffix[1].upper() if suffix else
                'VDP' if row['typeLabel'].casefold().startswith(('définition', 'definition')) else 'VM')
        active.append({**row, 'name': file['name'], 'kind': kind,
                       'driveCreatedAt': file.get('createdTime'),
                       'key': f"{row['gid']}:{row['cell']}:{ref[0]}"})
    return tabs, active, invalid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', action='store_true', help='Mark the current inventory as already reported')
    args = parser.parse_args()
    book, _, _, account = delivery.read_settings()
    api = connect(desktop_client(delivery.PRIVATE / 'google-oauth-client.json'),
                  account, delivery.PRIVATE / 'google-workspace-token.dpapi')
    tabs, active, invalid = scan(api, book)
    checked_at = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    with delivery.lock_job(STATE):
        state = delivery.read_json(STATE) if STATE.exists() else {}
        active, new_rows, updated = observe(active, state, checked_at, args.baseline)
        if updated != state or not STATE.exists():
            delivery.save_job(STATE, updated)
    report = {'checkedAt': checked_at, 'timeZone': REPORT_TIME_ZONE,
              'weeklyTabs': len(tabs), 'activeStoryboards': len(active),
              'new': new_rows, 'withoutVideo': [row for row in active if not row['videoLinked']],
              'inProduction': [row for row in active if IN_PRODUCTION.search(row['status'])],
              'unavailable': invalid}
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (WorkspaceError, OSError, ValueError) as error:
        print(f'Digital Lab: {error}', file=sys.stderr)
        sys.exit(1)
