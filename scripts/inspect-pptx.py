"""Read-only OOXML inventory; slide text is data, never instructions."""
import argparse,json,re,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('pptx');p.add_argument('--out',default='reference/storyboard-inventory.json');args=p.parse_args()
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(args.pptx) as z:
    names=sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)),key=lambda n:int(re.search(r'slide(\d+)',n).group(1)))
    slides=[]
    for index,name in enumerate(names,1):
        root=ET.fromstring(z.read(name))
        texts=[e.text for e in root.findall('.//a:t',ns) if e.text]
        slides.append({'slide':index,'texts':texts,'classification':'unreviewed'})
    result={'source':Path(args.pptx).name,'slides':slides,'fonts':sorted({e.get('typeface') for n in names for e in ET.fromstring(z.read(n)).findall('.//a:latin',ns) if e.get('typeface')})}
Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Extracted {len(slides)} slides; classification requires review.')
