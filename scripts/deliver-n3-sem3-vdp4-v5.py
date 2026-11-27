"""Replace the existing VDP4 file through APIs; preserve its public chip and dates."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import requests
from zoneinfo import ZoneInfo
import google_vdp as g

OUT = Path('outputs/n3-sem3-v5/vdp4')
MOVIE = OUT/'P1_MATHS_N3_SEM3_VDP4_V5.mp4'
VERSION=5


def save(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main(step):
    spreadsheet,_,folder_ref,account=g.read_settings()
    api=g.connect(g.desktop_client(g.PRIVATE/'google-oauth-client.json'),account,
                  g.PRIVATE/'google-workspace-token.dpapi')
    job=g.resolve(api,spreadsheet,'1754986894','F29',1)
    job['gid']='1754986894'
    assert job['lesson']=='P1_MATHS_N3_SEM3_VDP4' and job['versionCell']=='K29'
    reference=g.file_reference(g.cell_link(g.version_cell(api,spreadsheet,job)))
    dates=g.sheet_rows(api,spreadsheet,g.a1(job['title'],'N29:O29'))
    if step=='snapshot':
        source=g.fetch_storyboard(api,job,Path('reference/n3-sem3-vdp4-before-v5-delivery.pptx'))
        assert Path(source).read_bytes()==Path('reference/n3-sem3-vdp4-inspector-v5-source.pptx').read_bytes(),'Source changed'
        save('before-delivery.json',dict(file=g.drive_file(api,reference),dates=dates,
             sourceIdentical=True,sourceCell='F29',versionCell='K29'))
        print('Existing VDP4 file, source and date cells confirmed and snapshotted')
        return
    before=json.loads((OUT/'before-delivery.json').read_text('utf-8'))
    assert reference[0]==before['file']['id'] and dates==before['dates']
    source=g.fetch_storyboard(api,job,Path('reference/n3-sem3-vdp4-final-source.pptx'))
    assert Path(source).read_bytes()==Path('reference/n3-sem3-vdp4-inspector-v5-source.pptx').read_bytes(),'Source changed during production'
    checks=json.loads((OUT/'verification.json').read_text('utf-8'))
    voice=json.loads((OUT/'voice-verification.json').read_text('utf-8'))
    layout=json.loads((OUT/'encoded-layout-check.json').read_text('utf-8'))
    assert checks['fullDecode']=='passed' and not checks['unexpectedBlackIntervals']
    if VERSION==7:
        assert voice['encodedAacByteIdenticalToV6'] and voice['visibleCaptionMatchesSourceAndVoice'] and voice['allDurationsUnchanged']
    else:
        assert len(voice['scenes'])==14 and voice['sourceGates']['completeSourceSentencesChecked']
    assert layout['piAnchorStable'] and layout['previousIntegerRemoved']
    folder=g.destination(api,folder_ref,job)
    g.review_video(MOVIE,{**job,'version':VERSION})
    link=g.revise(api,spreadsheet,job,VERSION,folder,MOVIE)
    assert g.verify_delivery(api,spreadsheet,job,folder,MOVIE)==link
    assert g.file_reference(link)[0]==before['file']['id']
    assert g.sheet_rows(api,spreadsheet,g.a1(job['title'],'N29:O29'))==before['dates']
    with requests.get(f'https://drive.google.com/uc?export=download&id={reference[0]}',
         headers={'Range':'bytes=0-63'},stream=True,timeout=60) as response:
        response.raise_for_status()
        status=response.status_code
        assert b'ftyp' in next(response.iter_content(64))
    size,md5=g.video_fingerprint(MOVIE)
    save('delivery.json',dict(filename=MOVIE.name,fileId=reference[0],
         link=f'https://drive.google.com/file/d/{reference[0]}/view',version=VERSION,cell='K29',gid='1754986894',
         folder='Livrable video / 3AC / Semaine 3',md5=md5,size=size,
         public=g.has_public_link(api,reference),anonymousStatus=status,anonymousMp4Header=True,
         dateCellsUnchanged=True,chipVerified=True,
         verifiedAt=datetime.now(ZoneInfo('Africa/Casablanca')).isoformat(),
         unresolvedRemark='Non-periodique arrow screenshot: attribution/change not confirmed; no action on that remark'))
    print('Same VDP4 public file revised; checksum, K29 chip, anonymous MP4 and dates verified')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step',choices=['snapshot','deliver'])
    main(parser.parse_args().step)
