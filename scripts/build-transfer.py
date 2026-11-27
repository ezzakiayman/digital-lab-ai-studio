"""Build a private, credential-free project snapshot with a verified file manifest."""
import argparse,hashlib,json,re,shutil,zipfile
from datetime import datetime,timezone
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--destination',required=True);p.add_argument('--archive');p.add_argument('--reference-video');p.add_argument('--refresh',action='store_true')
p.add_argument('--reusable', action='store_true', help='Keep one example export and omit the original decks and full-length reference video.')
args=p.parse_args()
if args.reusable and args.reference_video:
 p.error('--reference-video is only for the full private snapshot')
root=Path(__file__).resolve().parent.parent;destination=Path(args.destination).resolve();marker=destination/'.digital-lab-transfer'
assert destination!=root and root not in destination.parents,'Place the portable project outside the original workspace.'
assert not destination.is_symlink(),'Do not write a snapshot through a symlink.'
transfer_format = 'digital-lab-reusable-transfer-v1' if args.reusable else 'digital-lab-private-transfer-v1'
if destination.exists():assert args.refresh and marker.is_file() and marker.read_text().strip()==transfer_format,'Use a new destination or refresh a snapshot of the same type.'
destination.mkdir(parents=True,exist_ok=True)
selected={}
def add(file,relative=None):
 if file.is_file():selected[relative or file.relative_to(root).as_posix()]=file
for name in ['.gitignore','AGENTS.md','START_HERE.md','NEXT_AGENT_PROMPT.md','PROJECT_HANDOFF.md','README.md','package.json','package-lock.json','next-env.d.ts','tsconfig.json','requirements-video.txt']:add(root/name)
for folder in ['src','scripts','docs','skill']:
 for file in (root/folder).rglob('*'):
  if file.is_file() and not any(part in {'private','__pycache__','.git'} for part in file.parts) and not file.name.startswith('.env'):add(file)
for name in ['brand','reference','n3','n3-paced','primes','primes-paced','primes-v2','primes-v2-paced','primes-review-2026-11-12','fractions','fractions-paced','polynomials-elevenlabs','polynomials-elevenlabs-paced','polynomials','polynomials-paced','polynomials-v2','polynomials-v2-paced','factorization','factorization-paced','factorization-v2','factorization-v2-paced','factorization-review-2026-11-12','fractions-v2','fractions-v2-paced','fractions-review-2026-11-12','like-terms','like-terms-paced','polynomial-subtraction','polynomial-subtraction-paced','signed-addition','signed-addition-paced','n3-sem3-paced','n3-sem3','n3-sem3-elevenlabs','n3-sem3-elevenlabs-paced']:
 for file in (root/'public'/name).rglob('*'):add(file)
if not args.reusable:
 for name in ['n3','n3-sem3','n3-sem2-vdp1','n3-sem2-vdp1-2026-11-10','n3-sem2-vdp2','n3-sem2-vdp3','n2-sem2-vdp1','n2-sem2-vdp1-2026-11-10','n2-sem2-vdp2','n2-sem2-vm4','n1-sem2-vdp2','n3-sem2-vdp2-2026-11-10','n3-sem2-vdp3-2026-11-10']:
  for file in (root/'reference'/name).rglob('*'):
   if not {'voice-review-originals','raw-voice'}.intersection(file.parts) and (file.suffix in {'.pptx','.json'} or 'slides' in file.parts or file.name.startswith('contact-')):add(file)
 for name in ['storyboard.pptx','storyboard-inventory.json']:add(root/'reference'/name)
for name in ['objective-2026-11-10','math-typesetting']:
 add(root/'reference'/name/'approved.png')
for name in ['simplifier.mp4','visual-evidence.json','asr.json','contact.jpg']:
 add(root/'reference/pronunciation-simplifier'/name)
if args.reusable:
 for name in ['P1_MATHS_N2_SEM2_VDP2.mp4','timeline.json','verification.json','export-termes-semblables.png','export-objectif.png']:
  add(root/'outputs/n2-sem2-vdp2'/name)
else:
 original=Path(args.reference_video).resolve() if args.reference_video else root/'reference/original-reference.mp4'
 if original.is_file():add(original,'reference/original-reference.mp4')
 for name in ['full','n3-v4','n3-sem2-vdp1-v4','n3-sem2-vdp1-2026-11-10','n3-sem2-vdp1-2026-11-12','n3-sem2-vdp3','n2-sem2-vdp1','n2-sem2-vdp1-google','n2-sem2-vdp1-2026-11-10','n3-sem2-vdp2','n2-sem2-vdp2','n2-sem2-vm4','n1-sem2-vdp2','n3-sem2-vdp2-2026-11-10','n3-sem2-vdp2-2026-11-12','n3-sem2-vdp3-2026-11-10','n3-sem2-vdp3-2026-11-12']:
  for file in (root/'outputs'/name).glob('*'):
   if file.suffix in {'.mp4','.json','.png'}:add(file)
 for batch in ('n3-sem3','n3-sem3-v2'):
  for i in range(1,5):
   for file in (root/'outputs'/batch/f'vdp{i}').glob('*'):
    if file.suffix in {'.mp4','.json'}:add(file)
records=[]
for name,source in sorted(selected.items()):
 parts=Path(name).parts
 assert not any(part in {'private','node_modules','.next','.git','__pycache__'} for part in parts),name
 assert not source.is_symlink() and not source.name.startswith('.env') and source.suffix!='.dpapi',name
 if source.suffix.lower() in {'.md','.json','.mjs','.ts','.tsx','.py','.ps1','.txt'}:
  text=source.read_text(encoding='utf-8')
  assert not re.search(r'AIza[0-9A-Za-z_-]{30,}|AQ\.[0-9A-Za-z_-]{30,}|sk-(?:proj-)?[0-9A-Za-z_-]{30,}|sk_[0-9A-Za-z]{35,}',text),'Credential-shaped value found; do not package '+name
 target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 digest=hashlib.sha256(source.read_bytes()).hexdigest();assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
 records.append(dict(path=name,bytes=target.stat().st_size,sha256=digest))
marker.write_text(transfer_format+'\n',encoding='utf-8')
manifest=dict(format=transfer_format,createdUtc=datetime.now(timezone.utc).isoformat(),includesCredentials=False,includesInstalledDependencies=False,includesModelWeights=False,sourceDecks=[r['path'] for r in records if r['path'].endswith('.pptx')],exampleVideos=[r['path'] for r in records if r['path'].startswith('outputs/') and r['path'].endswith('.mp4')],files=records,totalFileBytes=sum(r['bytes'] for r in records))
(destination/'TRANSFER_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if args.archive:
 archive=Path(args.archive).resolve();assert archive.parent!=destination and destination not in archive.parents,'Archive must be outside the project being archived.'
 archive.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name in [r['path'] for r in records]+['TRANSFER_MANIFEST.json','.digital-lab-transfer']:z.write(destination/name,arcname=destination.name+'/'+name)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  for r in records:assert hashlib.sha256(z.read(destination.name+'/'+r['path'])).hexdigest()==r['sha256'],r['path']
 checksum=hashlib.sha256(archive.read_bytes()).hexdigest();Path(str(archive)+'.sha256').write_text(checksum+'  '+archive.name+'\n',encoding='ascii')
 print('ZIP verified:',archive,'bytes:',archive.stat().st_size)
print('Snapshot verified:',destination,'files:',len(records),'bytes:',manifest['totalFileBytes'])
