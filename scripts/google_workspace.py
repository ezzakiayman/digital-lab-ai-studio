"""Google Workspace transport and one-time Desktop OAuth authorization."""

import base64
import ctypes
from ctypes import wintypes
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'private'
DRIVE = 'https://www.googleapis.com/drive/v3'
SHEETS = 'https://sheets.googleapis.com/v4/spreadsheets'
UPLOAD = 'https://www.googleapis.com/upload/drive/v3/files'
TOKEN = 'https://oauth2.googleapis.com/token'
SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/spreadsheets'


class WorkspaceError(Exception):
    pass


class GoogleError(WorkspaceError):
    def __init__(self, operation, status, reason):
        super().__init__(f'{operation}: Google HTTP {status} ({reason})')
        self.status = status


class TransportError(WorkspaceError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def error_reason(response):
    try:
        error = json.load(response).get('error', {})
        return error if isinstance(error, str) else error.get('status', 'request failed')
    except (ValueError, AttributeError):
        return 'request failed'


class Google:
    def __init__(self, token=''):
        self.token = token
        self.opener = build_opener(NoRedirect())

    def open(self, operation, url, *, method='GET', query=None, body=None, headers=None, allowed=()):
        if query:
            url += ('&' if '?' in url else '?') + urlencode(query, doseq=True)
        request_headers = dict(headers or {})
        if self.token:
            request_headers['Authorization'] = f'Bearer {self.token}'
        if isinstance(body, dict):
            request_headers['Content-Type'] = 'application/json'
            body = json.dumps(body).encode()
        request = Request(url, method=method, data=body, headers=request_headers)
        try:
            return self.opener.open(request, timeout=120)
        except HTTPError as error:
            if error.code in allowed:
                return error
            with error:
                raise GoogleError(operation, error.code, error_reason(error)) from None
        except (URLError, TimeoutError, ConnectionError):
            raise TransportError(f'{operation}: connection to Google interrupted') from None

    def json(self, operation, url, **kwargs):
        with self.open(operation, url, **kwargs) as response:
            return json.load(response)

    def verify_account(self, expected):
        result = self.json('Check Google account', DRIVE + '/about', query={'fields': 'user(emailAddress)'})
        if result.get('user', {}).get('emailAddress', '').casefold() != expected.casefold():
            raise WorkspaceError('Google authorization belongs to a different account')


def desktop_client(path):
    try:
        settings = json.loads(Path(path).read_text(encoding='utf-8-sig'))['installed']
        return {key: settings[key] for key in ('client_id', 'client_secret')}
    except (KeyError, FileNotFoundError, ValueError, TypeError):
        raise WorkspaceError('Provide the Google OAuth Desktop app JSON in private/google-oauth-client.json') from None


def token_request(client, **parameters):
    return Google().json('Google OAuth', TOKEN, method='POST',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         body=urlencode({**client, **parameters}).encode())


def dpapi(value, *, decrypt=False):
    class DataBlob(ctypes.Structure):
        _fields_ = [('size', wintypes.DWORD), ('data', ctypes.c_void_p)]

    raw = base64.b64decode(value, validate=True) if decrypt else value.encode()
    buffer = ctypes.create_string_buffer(raw)
    source = DataBlob(len(raw), ctypes.addressof(buffer))
    output = DataBlob()
    crypt = ctypes.WinDLL('crypt32', use_last_error=True)
    operation = crypt.CryptUnprotectData if decrypt else crypt.CryptProtectData
    operation.argtypes = (ctypes.POINTER(DataBlob), ctypes.c_void_p, ctypes.c_void_p,
                          ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DataBlob))
    operation.restype = wintypes.BOOL
    # CRYPTPROTECT_UI_FORBIDDEN with current-user protection.
    if not operation(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(output)):
        raise WorkspaceError('Windows could not access the current user’s protected Google authorization')
    free = ctypes.WinDLL('kernel32').LocalFree
    free.argtypes, free.restype = (ctypes.c_void_p,), ctypes.c_void_p
    try:
        result = ctypes.string_at(output.data, output.size)
        return result.decode() if decrypt else base64.b64encode(result).decode('ascii')
    finally:
        ctypes.memset(output.data, 0, output.size)
        free(output.data)


def authorize(client, account, token_path):
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(sha256(verifier.encode()).digest()).decode().rstrip('=')
    result = {}

    class Callback(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_GET(self):
            request = urlsplit(self.path)
            params = parse_qs(request.query)
            valid = request.path == '/oauth2/callback' and secrets.compare_digest(params.get('state', [''])[0], state)
            if valid:
                result['code'] = params.get('code', [''])[0]
            self.send_response(200 if valid else 404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            if valid:
                self.wfile.write(b'Return to the Digital Lab terminal to check the authorization result.')

    with HTTPServer(('127.0.0.1', 0), Callback) as server:
        redirect = f'http://127.0.0.1:{server.server_port}/oauth2/callback'
        query = urlencode({
            'client_id': client['client_id'], 'redirect_uri': redirect, 'response_type': 'code',
            'scope': SCOPES, 'state': state, 'code_challenge': challenge, 'code_challenge_method': 'S256',
            'access_type': 'offline', 'prompt': 'consent', 'login_hint': account,
        })
        print('Open this consent link yourself in your browser:', flush=True)
        print(f'https://accounts.google.com/o/oauth2/v2/auth?{query}', flush=True)
        server.timeout = 1
        deadline = monotonic() + 300
        while not result and monotonic() < deadline:
            server.handle_request()
    if not result.get('code'):
        raise WorkspaceError('Google consent was declined or timed out')
    granted = token_request(client, code=result['code'], code_verifier=verifier,
                            redirect_uri=redirect, grant_type='authorization_code')
    if not set(SCOPES.split()) <= set(granted.get('scope', '').split()) or not granted.get('refresh_token'):
        raise WorkspaceError('Google did not grant both scopes and offline access')
    Google(granted['access_token']).verify_account(account)
    token_path.parent.mkdir(parents=True, exist_ok=True)
    temp = token_path.with_suffix('.tmp')
    temp.write_text(dpapi(granted['refresh_token']), encoding='ascii')
    temp.replace(token_path)


def connect(client, account, token_path):
    try:
        protected = token_path.read_text(encoding='ascii')
    except FileNotFoundError:
        raise WorkspaceError('Run the Digital Lab auth command to authorize the work account first') from None
    granted = token_request(client, refresh_token=dpapi(protected, decrypt=True), grant_type='refresh_token')
    api = Google(granted['access_token'])
    api.verify_account(account)
    return api
