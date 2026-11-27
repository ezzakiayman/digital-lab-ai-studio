"""Exercise the Google delivery protocol without accessing real Drive or Sheets."""

from hashlib import md5
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
from queue import Queue
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import urlopen
from zipfile import ZipFile

import google_vdp as vdp
import google_workspace as workspace


VIDEO = 'P1_MATHS_N3_SEM3_VDP1.mp4'
SOURCE_LINK = 'https://drive.google.com/file/d/source/view'
VIDEO_LINK = 'https://drive.google.com/file/d/newvideo/view'
CHIP_LINK = VIDEO_LINK + '?usp=sharing'
SESSION = workspace.UPLOAD + '?upload_id=simulated'
BYTES = b'video from the renderer'


def video_chip(link=VIDEO_LINK):
    return {'userEnteredValue': {'stringValue': '@'},
            'chipRuns': [{'startIndex': 0, 'chip': {'richLinkProperties': {'uri': link}}}]}


class Response(BytesIO):
    def __init__(self, status=200, headers=None, data=b''):
        super().__init__(data)
        self.status, self.headers = status, headers or {}


class FakeGoogle:
    def __init__(self):
        self.cell = {}
        self.uploaded = False
        self.upload_starts = 0
        self.writes = 0
        self.interrupted = False
        self.upload_requests = []
        self.existing_video = None
        self.reservations = 0
        self.permissions = []
        self.shares = 0
        self.sharing_blocked = False
        self.delivery_cells = [{}, {}]
        self.stamp_writes = 0
        self.video = {
            'id': 'newvideo', 'parents': ['week3'], 'mimeType': 'video/mp4', 'name': VIDEO,
            'size': str(len(BYTES)), 'md5Checksum': md5(BYTES).hexdigest(), 'webViewLink': VIDEO_LINK,
            'createdTime': '2026-11-17T11:46:11.032Z',
        }
        self.workbook = {
            'properties': {'timeZone': 'Africa/Casablanca'},
            'sheets': [{'properties': {'sheetId': 7, 'title': "P1 / Semaine 3",
                                      'gridProperties': {'columnCount': 20, 'rowCount': 60}}}],
        }
        self.storyboard_link = SOURCE_LINK
        self.first_version_header = 'Version 1'

    def json(self, operation, url, *, query=None, body=None, method='GET', **_):
        if operation == 'Read tracker tabs':
            return self.workbook
        if operation == 'Read tracker cells':
            fields = query['fields']
            assert fields.count('(') == fields.count(')')
            if query['ranges'].endswith('!K8'):
                rows = [{'values': [self.cell]}]
            elif query['ranges'].endswith('!N8:O8'):
                rows = [{'values': self.delivery_cells}]
            else:
                header = [{}] * 17
                for column, label in ((5, 'Storyboard'), (10, self.first_version_header), (11, 'Version 2'),
                                      (13, 'Date '), (14, 'heure'), (15, 'Date '), (16, 'heure')):
                    header[column] = {'formattedValue': label}
                storyboard = {'chipRuns': [{'chip': {'richLinkProperties': {'uri': self.storyboard_link}}}]}
                rows = [{}, {'values': header}, {}, {}, {}, {}, {}, {'values': [{}] * 5 + [storyboard]}]
            return {'sheets': [{'data': [{'rowData': rows}]}]}
        if operation == 'Read Drive file':
            key = url.rsplit('/', 1)[-1]
            if key == 'source':
                return {'name': 'P1_MATHS_N3_SEM3_VDP1.pptx', 'mimeType': vdp.PPTX}
            if key == 'root':
                return {'id': 'root', 'mimeType': vdp.FOLDER}
            if key == 'newvideo' and self.uploaded:
                return self.video
            if key == 'newvideo' and self.existing_video:
                return self.existing_video
            raise workspace.GoogleError(operation, 404, 'NOT_FOUND')
        if operation == 'Find delivery folder':
            name = '3ac' if "'root'" in query['q'] and "'3AC'" in query['q'] else 'week3'
            return {'files': [{'id': name, 'mimeType': vdp.FOLDER}]}
        if operation == 'Reserve Drive file ID':
            self.reservations += 1
            return {'ids': ['newvideo']}
        if operation == 'Check public Drive link':
            assert method == 'GET' and url == workspace.DRIVE + '/files/newvideo/permissions'
            return {'permissions': self.permissions}
        if operation == 'Share MP4 with anyone who has the link':
            assert method == 'POST' and url == workspace.DRIVE + '/files/newvideo/permissions'
            assert body == {'type': 'anyone', 'role': 'reader', 'allowFileDiscovery': False}
            if self.sharing_blocked:
                raise workspace.GoogleError(operation, 403, 'PERMISSION_DENIED')
            self.permissions.append(body)
            self.shares += 1
            return body
        if operation == 'Write original MP4 delivery date and time':
            assert method == 'POST' and url == workspace.SHEETS + '/sheet:batchUpdate'
            assert vdp.video_chip_link(self.cell)
            for request in body['requests']:
                update = request['updateCells']
                start = update['start']
                assert (start['sheetId'], start['rowIndex']) == (7, 7)
                offset = start['columnIndex'] - 13
                assert offset in (0, 1) and not self.delivery_cells[offset]
                value = update['rows'][0]['values'][0]
                assert value['userEnteredFormat']['numberFormat']['type'] == ('DATE', 'TIME')[offset]
                self.delivery_cells[offset] = value
                self.stamp_writes += 1
            return {}
        if operation == 'Write MP4 file chip to tracker':
            assert any(p['type'] == 'anyone' and p['role'] == 'reader' for p in self.permissions)
            assert method == 'POST' and url == workspace.SHEETS + '/sheet:batchUpdate'
            assert body == {'requests': [{'updateCells': {
                'start': {'sheetId': 7, 'rowIndex': 7, 'columnIndex': 10},
                'rows': [{'values': [video_chip()]}],
                'fields': 'userEnteredValue,chipRuns',
            }}]}
            self.writes += 1
            self.cell = {
                'userEnteredValue': {'stringValue': VIDEO},
                'formattedValue': VIDEO,
                'chipRuns': [{'chip': {'richLinkProperties': {'uri': CHIP_LINK}}}],
            }
            return {}
        raise AssertionError(operation)

    def open(self, operation, url, *, headers=None, body=None, method='GET', **_):
        if operation == 'Download storyboard':
            result = BytesIO()
            with ZipFile(result, 'w') as zip_file:
                zip_file.writestr('ppt/presentation.xml', '<presentation/>')
            return Response(data=result.getvalue())
        if operation == 'Start resumable MP4 upload':
            if self.existing_video:
                assert (method, url, body) == ('PATCH', workspace.UPLOAD + '/newvideo', {'name': self.video['name']})
            else:
                assert method == 'POST' and body['parents'] == ['week3'] and body['name'] == VIDEO
            self.upload_starts += 1
            return Response(headers={'Location': SESSION})
        assert url == SESSION
        self.upload_requests.append((headers['Content-Range'], body))
        if not self.interrupted:
            self.interrupted = True
            raise workspace.TransportError('simulated interrupted connection')
        if body == b'':
            return Response(308, {'Range': 'bytes=0-6'})
        assert body == BYTES[7:]
        self.uploaded = True
        return Response(201)


class DeliveryTests(TestCase):
    def setUp(self):
        self.api = FakeGoogle()
        self.job = vdp.resolve(self.api, 'sheet', '7', 'F8', 1)
        self.job['gid'] = '7'
        self.folder = vdp.destination(self.api, ('root', ''), self.job)
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.video = self.path / VIDEO
        self.video.write_bytes(BYTES)

    def test_video1_header_resolves_to_the_existing_first_version_column(self):
        self.api.first_version_header = 'video1'
        self.assertEqual(vdp.resolve(self.api, 'sheet', '7', 'F8', 1)['versionCell'], 'K8')
        self.assertEqual(vdp.resolve(self.api, 'sheet', '7', 'F8', 2)['versionCell'], 'L8')

    def publish(self):
        with patch.object(vdp, 'PRIVATE', self.path):
            return vdp.deliver(self.api, 'sheet', '7', self.job, self.folder, self.video)

    def test_full_route_download_resume_verify_and_retry(self):
        self.assertEqual((self.job['lesson'], self.job['versionCell'], self.folder['id']),
                         ('P1_MATHS_N3_SEM3_VDP1', 'K8', 'week3'))
        deck = self.path / 'source.pptx'
        self.assertEqual(vdp.fetch_storyboard(self.api, self.job, deck), deck)
        self.assertEqual(self.publish(), CHIP_LINK)
        self.assertEqual(self.api.upload_requests, [
            (f'bytes 0-{len(BYTES) - 1}/{len(BYTES)}', BYTES),
            (f'bytes */{len(BYTES)}', b''),
            (f'bytes 7-{len(BYTES) - 1}/{len(BYTES)}', BYTES[7:]),
        ])
        self.assertEqual(vdp.verify_delivery(self.api, 'sheet', self.job, self.folder, self.video), CHIP_LINK)
        self.assertEqual(self.publish(), CHIP_LINK)
        self.assertEqual((self.api.upload_starts, self.api.writes, self.api.shares, self.api.stamp_writes), (1, 1, 1, 2))
        self.assertEqual([c['userEnteredValue']['numberValue'] for c in self.api.delivery_cells],
                         [46343, (12 * 60 + 46) / 1440])
        [receipt] = (self.path / 'google-deliveries').glob('*.json')
        self.assertNotIn('session', json.loads(receipt.read_text(encoding='utf-8')))

    def test_sharing_failure_keeps_tracker_empty_and_retries_same_file(self):
        self.api.sharing_blocked = True
        with self.assertRaises(workspace.GoogleError):
            self.publish()
        self.assertEqual((self.api.upload_starts, self.api.writes), (1, 0))
        self.api.sharing_blocked = False
        self.assertEqual(self.publish(), CHIP_LINK)
        self.assertEqual((self.api.upload_starts, self.api.writes, self.api.shares), (1, 1, 1))

    def test_existing_restricted_link_is_detected_and_repaired_in_place(self):
        self.api.uploaded = True
        self.api.cell = {'hyperlink': VIDEO_LINK}
        self.api.permissions = [{'type': 'anyone', 'role': 'reader', 'view': 'metadata'}]
        with self.assertRaisesRegex(workspace.WorkspaceError, 'restricted'):
            vdp.verify_delivery(self.api, 'sheet', self.job, self.folder, self.video)
        self.assertEqual(self.publish(), CHIP_LINK)
        self.assertEqual(vdp.verify_delivery(self.api, 'sheet', self.job, self.folder, self.video), CHIP_LINK)
        self.assertEqual((self.api.upload_starts, self.api.writes, self.api.shares), (0, 1, 1))

    def test_repeat_delivery_preserves_dates_already_in_the_tracker(self):
        self.api.uploaded = True
        self.api.cell = video_chip(CHIP_LINK)
        self.api.delivery_cells = [{'userEnteredValue': {'numberValue': 46342}},
                                   {'userEnteredValue': {'numberValue': .5}}]
        self.assertEqual(self.publish(), CHIP_LINK)
        self.assertEqual((self.api.upload_starts, self.api.writes, self.api.stamp_writes), (0, 0, 0))

    def test_sheet_write_failure_reuses_the_uploaded_file(self):
        original = self.api.json

        def reject_write(operation, *args, **kwargs):
            if operation == 'Write MP4 file chip to tracker':
                raise workspace.GoogleError(operation, 503, 'UNAVAILABLE')
            return original(operation, *args, **kwargs)

        with patch.object(self.api, 'json', side_effect=reject_write):
            with self.assertRaises(workspace.GoogleError):
                self.publish()
        self.assertEqual(self.publish(), CHIP_LINK)
        self.assertEqual((self.api.upload_starts, self.api.writes), (1, 1))

    def test_protect_existing_cell_including_a_formula_displayed_as_blank(self):
        self.api.cell = {'userEnteredValue': {'formulaValue': '=""'}}
        with self.assertRaisesRegex(workspace.WorkspaceError, 'already contains'):
            self.publish()
        self.assertEqual((self.api.upload_starts, self.api.writes), (0, 0))

    def test_drive_fingerprint_mismatch_leaves_tracker_empty(self):
        self.api.video['md5Checksum'] = 'wrong'
        with self.assertRaisesRegex(workspace.WorkspaceError, 'expected MP4 bytes'):
            self.publish()
        self.assertEqual(self.api.writes, 0)

    def test_revision_upload_updates_same_drive_id_and_keeps_sheet_link(self):
        self.api.existing_video = {**self.api.video, 'md5Checksum': 'old-checksum',
                                   'capabilities': {'canModifyContent': True}}
        self.api.cell = video_chip(CHIP_LINK)
        revision = self.path / 'P1_MATHS_N3_SEM3_VDP1_V2.mp4'
        revision.write_bytes(BYTES)
        self.api.video['name'] = revision.name
        with patch.object(vdp, 'PRIVATE', self.path):
            self.assertEqual(vdp.revise(self.api, 'sheet', self.job, 2, self.folder, revision), CHIP_LINK)
            self.assertEqual(vdp.revise(self.api, 'sheet', self.job, 2, self.folder, revision), CHIP_LINK)
        self.assertEqual((self.api.upload_starts, self.api.reservations, self.api.writes, self.api.shares),
                         (1, 0, 0, 1))

    def test_new_storyboard_link_detected_before_sheet_write(self):
        def change_link(*args, **kwargs):
            self.api.uploaded = True
            self.api.storyboard_link = 'https://drive.google.com/file/d/wrong/view'

        with patch.object(vdp, 'upload', side_effect=change_link):
            with self.assertRaises(workspace.GoogleError):
                self.publish()
        self.assertEqual(self.api.writes, 0)

    def test_dpapi_roundtrip(self):
        sample = 'synthetic-refresh-token'
        encrypted = workspace.dpapi(sample)
        self.assertNotIn(sample, encrypted)
        self.assertEqual(workspace.dpapi(encrypted, decrypt=True), sample)

    def test_desktop_oauth_loopback_and_refresh(self):
        messages = Queue()
        client = {'client_id': 'desktop-test', 'client_secret': 'test-only'}
        account = 'test@example.invalid'
        token_path = self.path / 'work-token.dpapi'
        granted = {'access_token': 'access-test', 'refresh_token': 'refresh-test', 'scope': workspace.SCOPES}
        with patch('builtins.print', side_effect=lambda message, **_: messages.put(message)), \
                patch.object(workspace, 'token_request', return_value=granted) as token, \
                patch.object(workspace.Google, 'verify_account') as verify, \
                ThreadPoolExecutor(1) as task:
            flow = task.submit(workspace.authorize, client, account, token_path)
            self.assertIn('consent link', messages.get(timeout=5))
            query = parse_qs(urlsplit(messages.get(timeout=5)).query)
            self.assertEqual(query['code_challenge_method'], ['S256'])
            callback = query['redirect_uri'][0] + '?' + urlencode({'state': query['state'][0], 'code': 'consent-test'})
            with urlopen(callback, timeout=5) as response:
                self.assertEqual(response.status, 200)
            flow.result(timeout=5)
            token.assert_called_once()
            self.assertEqual(token.call_args.kwargs['code'], 'consent-test')
            self.assertNotIn('refresh-test', token_path.read_text(encoding='ascii'))
            api = workspace.connect(client, account, token_path)
            self.assertEqual(api.token, 'access-test')
            self.assertEqual(token.call_args.kwargs['refresh_token'], 'refresh-test')
            self.assertEqual(verify.call_count, 2)


if __name__ == '__main__':
    main()
