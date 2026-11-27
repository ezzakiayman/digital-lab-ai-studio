"""Check the handoff's original files before editing; installed extra files are allowed."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'TRANSFER_MANIFEST.json').read_text(encoding='utf-8'));failures=[]
for record in manifest['files']:
 file=(root/record['path']).resolve()
 if root not in file.parents:raise RuntimeError('Manifest path outside project')
 if not file.is_file() or file.stat().st_size!=record['bytes'] or hashlib.sha256(file.read_bytes()).hexdigest()!=record['sha256']:failures.append(record['path'])
if failures:raise RuntimeError('Missing/changed snapshot files: '+', '.join(failures))
print('Verified',len(manifest['files']),'original snapshot files; credentials, installed dependencies and model weights are not included.')
