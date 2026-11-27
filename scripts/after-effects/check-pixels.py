"""Compare the layer-data reconstruction to checked frames from the published MP4."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def image_data(path):
    with Image.open(path) as im:
        return im.convert('RGB').resize((960,540),Image.Resampling.LANCZOS)


def mask_image(im):
    return Image.fromarray((np.asarray(im).min(axis=2)<208).astype(np.uint8)*255)


def scores(reference, comparison):
    a=mask_image(reference)
    b=mask_image(comparison)
    A=np.asarray(a)>0
    B=np.asarray(b)>0
    near_a=np.asarray(a.filter(ImageFilter.MaxFilter(5)))>0
    near_b=np.asarray(b.filter(ImageFilter.MaxFilter(5)))>0
    union=A|B
    colour=np.abs(np.asarray(reference).astype(float)-np.asarray(comparison).astype(float)).mean(axis=2)
    recall=(A&near_b).sum()/max(1,A.sum())
    precision=(B&near_a).sum()/max(1,B.sum())
    return {'inkRecall':round(float(recall),4),'inkPrecision':round(float(precision),4),
            'inkIoU':round((A&B).sum()/max(1,union.sum()),4),
            'inkMeanError255':round(float(colour[union].mean()),2) if union.any() else 0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('qa',type=Path)
    parser.add_argument('references',type=Path)
    args=parser.parse_args()
    rows=[]
    for p in sorted((args.qa/'renders').glob('f*.png')):
        ref=args.references/(p.stem+'.jpg')
        if ref.is_file():
            rows.append(dict(frame=int(p.stem[1:]),**scores(image_data(ref),image_data(p))))
    if not rows:
        raise ValueError('Missing matching reference frames')
    ranked=sorted(rows,key=lambda row:min(row['inkPrecision'],row['inkRecall']))
    montage=Image.new('RGB',(900,1580),'#ebedf0')
    for i,row in enumerate(ranked[:6]):
        base='f'+str(row['frame']).zfill(6)
        for column,p in enumerate([args.references/(base+'.jpg'),args.qa/'renders'/(base+'.png')]):
            with Image.open(p) as im:
                montage.paste(im.convert('RGB').resize((440,247),Image.Resampling.LANCZOS),(column*450,i*263))
        ImageDraw.Draw(montage).text((5,i*263+248),f"{base}  source / reconstruction   {row['inkRecall']:.3f}  {row['inkPrecision']:.3f}",fill='black')
    montage.save(args.qa/'worst-comparisons.jpg',quality=88)
    result=dict(frameCount=len(rows),method='Chromium vector replay of portable layer data; known original decoded frames. Nonwhite masks on 960x540 images with 2px tolerance.',frames=rows)
    (args.qa/'visual-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Compared',len(rows),'frames. Lowest ink recall and precision:',min(r['inkRecall'] for r in rows),min(r['inkPrecision'] for r in rows))
    print('Lowest-scoring frames:',ranked[:5])


if __name__=='__main__':
    main()

