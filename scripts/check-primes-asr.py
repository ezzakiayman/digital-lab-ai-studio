"""Check spoken range boundaries and each prime against separate local ASR output."""
import argparse,json,re,hashlib
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--asr-dir',default='reference/n3-sem2-vdp1/asr')
p.add_argument('--plan',default='src/video/primes-plan.json')
args=p.parse_args()
root=Path(args.asr_dir)
plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
for scene in plan['scenes']:
    review=json.loads((root/(scene['id']+'.json')).read_text(encoding='utf-8'))
    signature=hashlib.sha256((Path('public')/scene['audio']).read_bytes()+b'whisper-small-fr').hexdigest()
    assert review['signature']==signature,'Stale or incomplete ASR review: '+scene['id']
expected={
 'premiers-2-47':[10,2,3,5,7,10,20,11,13,17,19,20,30,23,29,30,40,31,37,40,50,41,43,47],
 'premiers-53-97':[50,60,53,59,60,70,61,67,70,80,71,73,79,80,90,83,89,90,100,97],
}
for id,numbers in expected.items():
    text=json.loads((root/(id+'.json')).read_text(encoding='utf-8'))['transcript']
    actual=[int(n) for n in re.findall(r'\d+',text)]
    assert actual==numbers,(id,actual)
definition=json.loads((root/'definition.json').read_text(encoding='utf-8'))['transcript']
example=json.loads((root/'exemple-10.json').read_text(encoding='utf-8'))['transcript']
assert 'possède exactement 2 diviseurs positifs distincts' in definition
assert 'Il possède 4 diviseurs positifs au lieu de 2' in example
report=dict(recordingsReviewed=len(plan['scenes']),model='faster-whisper small, CPU int8',method='Independent ASR without the expected narration as a decoding prompt',primeListsAndRangeBounds='All 25 primes and all spoken range boundaries recovered in the expected order',clarifiedPassages='Definition and 10-example regenerated with clearer wording; final independent ASR recovered the exact two-divisor criterion and four-divisors-instead-of-two conclusion',limits='ASR remains a review aid with French homophone and Arabic transliteration limits, not a complete pronunciation certificate. Forced alignment separately uses the known text. Cloud cross-check unavailable (404 on old model, 503 on current models).')
if plan['scenes'][0].get('revision')=='2026-11-10':
    pronunciation=json.loads((root/'prononciation.json').read_text(encoding='utf-8'))['transcript']
    assert re.search(r'\bpre[\s,.-]+mier[\s,.-]+premier\b',pronunciation,re.IGNORECASE),pronunciation
    report.update(pronunciation='Independent ASR recovered the separate syllables and then the full word.',
                  clarifiedPassages='The reused definition and 10-example match their reviewed audio receipts.',
                  limits='ASR is a review aid with French homophone and Arabic transliteration limits. Forced alignment separately uses the known text.')
(root.parent/'audio-review-summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['primeListsAndRangeBounds'])
