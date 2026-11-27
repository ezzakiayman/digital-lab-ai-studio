"""Prepare a source-only GitHub snapshot; never copy production media or credentials."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]
BLOCKED_PARTS={'private','node_modules','.git','.next','__pycache__','.npm-cache','.venv'}
CODE_EXT={'.ts','.tsx','.css','.json','.py','.mjs','.ps1','.md','.iss','.yml','.yaml','.txt'}
SECRETS=re.compile(r'AIza[0-9A-Za-z_-]{30,}|AQ\.[0-9A-Za-z_-]{30,}|sk-(?:proj-)?[0-9A-Za-z_-]{30,}|sk_[0-9A-Za-z]{35,}|gh[opusr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
OAUTH=re.compile(r'"(?:refresh_token|client_secret|access_token)"\s*:\s*"[^"\s]{12,}"')

def is_source_code(relative):
    return (relative.suffix in CODE_EXT or
            relative.parts[:2] == ('scripts', 'after-effects') and relative.suffix in {'.js', '.jsx'})

def scrub(value):
    if isinstance(value,dict):
        return {k:scrub(v) for k,v in value.items() if k!='pronunciationDictionaryLocators'}
    if isinstance(value,list):return [scrub(v) for v in value]
    return value

def build(destination):
    destination=destination.resolve()
    assert ROOT in destination.parents and destination!=ROOT,'Use a generated folder within this workspace'
    marker=destination/'.digital-lab-github-snapshot'
    assert not destination.is_symlink()
    if destination.exists():assert marker.is_file(),'Refuse to overwrite an unrelated directory'
    selected={}
    for name in ['.gitignore','.gitattributes','AGENTS.md','START_HERE.md','NEXT_AGENT_PROMPT.md','PROJECT_HANDOFF.md','README.md','package.json','package-lock.json','next-env.d.ts','tsconfig.json','requirements-video.txt']:
        selected[name]=ROOT/name
    for folder in ['src','scripts','docs','skill','.github','prototype']:
        for f in (ROOT/folder).rglob('*'):
            relative=f.relative_to(ROOT)
            if f.is_file() and is_source_code(relative) and not BLOCKED_PARTS.intersection(relative.parts):
                selected[relative.as_posix()]=f
    for name in ['public/brand/objective-target.png','public/brand/question-mark.png','public/demo/silence.wav']:
        selected[name]=ROOT/name
    records=[];redacted=[]
    for name,source in sorted(selected.items()):
        assert source.is_file() and not source.is_symlink(),name
        assert not BLOCKED_PARTS.intersection(Path(name).parts),name
        raw=source.read_bytes()
        if is_source_code(Path(name)):
            text=raw.decode('utf-8-sig')
            assert not SECRETS.search(text) and not OAUTH.search(text),'Potential credential in '+name
            if source.suffix=='.json' and 'pronunciationDictionaryLocators' in text:
                raw=(json.dumps(scrub(json.loads(text)),ensure_ascii=False,indent=2)+'\n').encode('utf-8')
                redacted.append(name)
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        records.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    marker.write_text('digital-lab-github-source-v1\n',encoding='utf-8')
    manifest=dict(format='digital-lab-github-source-v1',createdUtc=datetime.now(timezone.utc).isoformat(),
        includesProductionMedia=False,includesCredentials=False,includesPrivateDictionaries=False,
        redactedPrivateDictionaryPlans=redacted,files=records,totalBytes=sum(r['bytes'] for r in records))
    (destination/'GITHUB_SNAPSHOT_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Source-only snapshot: {len(records)} files, {manifest["totalBytes"]} bytes; {len(redacted)} private dictionary plans scrubbed')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination',type=Path,required=True)
    build(parser.parse_args().destination)
