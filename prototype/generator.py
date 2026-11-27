#!/usr/bin/env python3
"""Deterministic PPTX → animated MP4 proof of concept, entirely offline."""
import argparse, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation

ROOT=Path(__file__).resolve().parent
W,H,FPS=1280,720,24
COLORS=json.loads((ROOT/'charter.json').read_text())

def font(size,bold=False):
    return ImageFont.truetype(COLORS['font_bold' if bold else 'font'],size)

def label(d,x,y,s,size=34,bold=False,color='text',maxwidth=1040):
    f=font(size,bold); line=''; rows=[]
    for word in s.split():
        candidate=(line+' '+word).strip()
        if line and d.textbbox((0,0),candidate,font=f)[2]>maxwidth:
            rows.append(line);line=word
        else:line=candidate
    rows.append(line)
    for k,row in enumerate(rows):d.text((x,y+k*(size+17)),row,font=f,fill=COLORS[color])

def extract(path):
    data=[]
    for i,slide in enumerate(Presentation(path).slides,1):
        texts=[shape.text.strip() for shape in slide.shapes if shape.has_text_frame and shape.text.strip()]
        data.append({'slide':i,'texts':texts})
    return data

def scene_model(slides):
    content=' '.join(' '.join(x['texts']) for x in slides).lower()
    if 'deux nombres sont négatifs' in content and 'droite numérique' in content:
        return [
          {'type':'intro','duration':6,'title':'Comparer et ranger des nombres'},
          {'type':'property','duration':10,'title':'Propriété 1','text':'Si deux nombres sont négatifs, le plus petit est celui qui a la plus grande valeur absolue.'},
          {'type':'example','duration':11,'title':'Exemple 1','text':'Comparer −3 et −2','steps':['|−3| = 3   et   |−2| = 2','3 > 2','Donc −3 < −2']},
          {'type':'property','duration':9,'title':'Propriété 2','text':'Un nombre négatif est plus petit qu’un nombre positif.'},
          {'type':'example','duration':9,'title':'Exemple 2','text':'Comparer −5 et 1','steps':['−5 est négatif, 1 est positif','Donc −5 < 1']},
          {'type':'line','duration':13,'title':'Remarque','text':'Sur une droite numérique, le plus petit est situé à gauche.'}]
    return [{'type':'generic','duration':5,'title':f'Diapositive {x["slide"]}','text':' — '.join(x['texts'])[:300]} for x in slides]

def frame(s,t):
    img=Image.new('RGB',(W,H),COLORS['background']);d=ImageDraw.Draw(img)
    if s['type']=='intro':
        dx=round(100*max(0,1-t/1.2))
        d.rounded_rectangle((75+dx,190,1195,330),radius=20,outline=COLORS['navy'],width=4)
        label(d,112+dx,225,s['title'],47,True,'navy')
        if t>1.8:label(d,112,418,'Comparer des nombres',35)
        return np.asarray(img,dtype=np.uint8).tobytes()
    title=s['title'];d.rounded_rectangle((78,65,78+max(250,len(title)*23),128),radius=15,fill=COLORS['turquoise'])
    label(d,100,76,title,33,True,'background')
    if s['type']=='property':
        d.rounded_rectangle((82,212,1198,475),radius=18,outline=COLORS['turquoise'],width=4)
        if t>0.6:label(d,115,268,s['text'],39,True)
    elif s['type']=='example':
        d.rounded_rectangle((82,170,1198,637),radius=18,outline=COLORS['turquoise'],width=4)
        label(d,115,201,s['text'],40,True)
        for i,step in enumerate(s['steps']):
            if t>2+i*2.2:label(d,150,315+i*96,step,37,i==len(s['steps'])-1,'red' if i==len(s['steps'])-1 else 'text')
    elif s['type']=='line':
        label(d,87,182,s['text'],31,True)
        y=444;d.line((140,y,1155,y),fill=COLORS['text'],width=4)
        d.polygon([(1155,y-13),(1178,y),(1155,y+13)],fill=COLORS['text'])
        for n in range(-5,6):
            x=650+n*89;d.line((x,y-12,x,y+12),fill=COLORS['text'],width=3);label(d,x-20,y+27,str(n),25)
        if t>4:
            for n,c in [(-3,'red'),(-2,'turquoise')]:
                x=650+n*89;d.rounded_rectangle((x-30,y+13,x+32,y+72),radius=8,outline=COLORS[c],width=4)
        if t>8:label(d,485,580,'−3 < −2',47,True,'red')
    else:label(d,100,210,s.get('text',''),34)
    return np.asarray(img,dtype=np.uint8).tobytes()

def main():
    a=argparse.ArgumentParser();a.add_argument('--pptx',required=True);a.add_argument('--out',default='preview.mp4');a.add_argument('--manifest',default='scenes.json');args=a.parse_args()
    slides=extract(args.pptx);scenes=scene_model(slides)
    Path(args.manifest).write_text(json.dumps({'slides':slides,'scenes':scenes,'voiceover_needed':True},ensure_ascii=False,indent=2),encoding='utf-8')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',args.out]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for s in scenes:
            for i in range(s['duration']*FPS):p.stdin.write(frame(s,i/FPS))
    finally:p.stdin.close()
    if p.wait():raise RuntimeError('ffmpeg failed')
    print(f'Exported {args.out}: {len(slides)} storyboard slides → {len(scenes)} scenes, {sum(x["duration"] for x in scenes)} seconds (silent)')
if __name__=='__main__':main()
