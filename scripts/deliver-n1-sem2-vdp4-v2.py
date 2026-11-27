"""Publish the sign correction as a revision of the existing public K24 file."""
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo
import requests
import google_vdp as g

OUT=Path('outputs/n1-sem2-vdp4-v2')
MOVIE=OUT/'P1_MATHS_N1_SEM2_VDP4_V2.mp4'
before=json.loads((OUT/'before-delivery.json').read_text('utf-8'))
checks=json.loads((OUT/'verification.json').read_text('utf-8'))
voice=json.loads((OUT/'voice-verification.json').read_text('utf-8'))
assert checks['fullDecode']=='passed' and not checks['unexpectedBlackIntervals']
assert voice['encodedAacByteIdenticalToV1'] and voice['onlyTwoApprovedVisualChanges']
spreadsheet,_,folder_ref,account=g.read_settings()
api=g.connect(g.desktop_client(g.PRIVATE/'google-oauth-client.json'),account,g.PRIVATE/'google-workspace-token.dpapi')
job=g.resolve(api,spreadsheet,'1191794673','F24',1);job['gid']='1191794673'
assert job['lesson']=='P1_MATHS_N1_SEM2_VDP4' and job['versionCell']=='K24'
reference=g.file_reference(g.cell_link(g.version_cell(api,spreadsheet,job)))
assert reference[0]==before['file']['id']
dates=g.sheet_rows(api,spreadsheet,g.a1(job['title'],'N24:O24'))
assert dates==before['dates']
source=g.fetch_storyboard(api,job,OUT/'source-final.pptx')
assert Path(source).read_bytes()==(OUT/'source-before.pptx').read_bytes()
assert before['sourceIdentical']
folder=g.destination(api,folder_ref,job)
g.review_video(MOVIE,{**job,'version':2})
link=g.revise(api,spreadsheet,job,2,folder,MOVIE)
assert g.verify_delivery(api,spreadsheet,job,folder,MOVIE)==link
assert g.file_reference(link)[0]==reference[0]
assert g.sheet_rows(api,spreadsheet,g.a1(job['title'],'N24:O24'))==dates
with requests.get(f'https://drive.google.com/uc?export=download&id={reference[0]}',headers={'Range':'bytes=0-63'},stream=True,timeout=60) as response:
    response.raise_for_status();status=response.status_code
    assert b'ftyp' in next(response.iter_content(64))
size,md5=g.video_fingerprint(MOVIE)
result=dict(filename=MOVIE.name,fileId=reference[0],link=f'https://drive.google.com/file/d/{reference[0]}/view',version=2,
    cell='K24',gid='1191794673',folder='Livrable video / 1AC / Semaine 2',md5=md5,size=size,
    public=g.has_public_link(api,reference),anonymousStatus=status,anonymousMp4Header=True,
    dateCellsUnchanged=True,chipVerified=True,verifiedAt=datetime.now(ZoneInfo('Africa/Casablanca')).isoformat())
(OUT/'delivery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Existing public file revised; checksum, K24 chip, dates and anonymous MP4 verified')
