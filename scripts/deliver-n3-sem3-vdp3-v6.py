"""Revise the existing public VDP3 file after local verification, preserving dates."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import requests
from zoneinfo import ZoneInfo
import google_vdp as g

OUT = Path('outputs/n3-sem3-v6/vdp3')
MOVIE = OUT / 'P1_MATHS_N3_SEM3_VDP3_V6.mp4'
FILE_ID = '1RkeDcRYVi3vc4U2Oy6vf5M2EG461WwCx'


def save(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main(step):
    spreadsheet, _, folder_ref, account = g.read_settings()
    api = g.connect(g.desktop_client(g.PRIVATE / 'google-oauth-client.json'), account,
                    g.PRIVATE / 'google-workspace-token.dpapi')
    job = g.resolve(api, spreadsheet, '1754986894', 'F22', 1)
    job['gid'] = '1754986894'
    assert job['lesson'] == 'P1_MATHS_N3_SEM3_VDP3' and job['versionCell'] == 'K22'
    cell = g.version_cell(api, spreadsheet, job)
    reference = g.file_reference(g.cell_link(cell))
    assert reference[0] == FILE_ID
    dates = g.sheet_rows(api, spreadsheet, g.a1(job['title'], 'N22:O22'))
    if step == 'snapshot':
        source = g.fetch_storyboard(api, job, Path('reference/n3-sem3-vdp3-v6-source.pptx'))
        assert Path(source).read_bytes() == Path('reference/n3-sem3-vdp3-inspector-v5-source.pptx').read_bytes(), 'Source changed'
        save('before-delivery.json', dict(file=g.drive_file(api, reference), dates=dates,
             sourceIdenticalToV5=True, sourceCell='F22', versionCell='K22'))
        print('Same source confirmed; existing public file and date cells snapshotted')
        return
    before = json.loads((OUT / 'before-delivery.json').read_text('utf-8'))
    assert before['dates'] == dates, 'Tracker dates changed since snapshot'
    voice = json.loads((OUT / 'voice-verification.json').read_text('utf-8'))
    checks = json.loads((OUT / 'verification.json').read_text('utf-8'))
    layout = json.loads((OUT / 'encoded-layout-check.json').read_text('utf-8'))
    assert voice['encodedAacByteIdenticalToV5']
    assert checks['fullDecode'] == 'passed' and not checks['unexpectedBlackIntervals']
    assert layout['deltaPixels'] <= 1.5 and layout['lowerAreaContinuousFramesChecked'] == 376
    folder = g.destination(api, folder_ref, job)
    g.review_video(MOVIE, {**job, 'version': 6})
    link = g.revise(api, spreadsheet, job, 6, folder, MOVIE)
    assert g.file_reference(link)[0] == FILE_ID
    assert g.verify_delivery(api, spreadsheet, job, folder, MOVIE) == link
    assert g.sheet_rows(api, spreadsheet, g.a1(job['title'], 'N22:O22')) == before['dates']
    url = f'https://drive.google.com/uc?export=download&id={FILE_ID}'
    with requests.get(url, headers={'Range': 'bytes=0-63'}, stream=True, timeout=60) as response:
        response.raise_for_status()
        header = next(response.iter_content(64))
        anonymous_status = response.status_code
    assert b'ftyp' in header, 'Anonymous URL did not return MP4'
    size, md5 = g.video_fingerprint(MOVIE)
    save('delivery.json', dict(filename=MOVIE.name, link=f'https://drive.google.com/file/d/{FILE_ID}/view',
         fileId=FILE_ID, version=6, cell='K22', gid='1754986894',
         folder='Livrable video / 3AC / Semaine 3', md5=md5, size=size,
         public=g.has_public_link(api, reference), anonymousStatus=anonymous_status,
         anonymousMp4Header=True, dateCellsUnchanged=True, chipVerified=True,
         verifiedAt=datetime.now(ZoneInfo('Africa/Casablanca')).isoformat()))
    print('V6 revised in the same public file; checksum, chip, anonymous MP4 and unchanged dates verified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step', choices=['snapshot', 'deliver'])
    main(parser.parse_args().step)
