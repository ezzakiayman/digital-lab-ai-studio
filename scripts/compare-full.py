import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path('outputs/full');times=[10,37,52,85,120,132,145,165,175];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
contact=Image.new('RGB',(1920,300*5),'#122638')
for i,t in enumerate(times):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i','C:/Users/EDITO/Downloads/P1_MATHS_N1_SEM1_VDP4.mp4','-frames:v','1','-y',str(root/f'original-{t}.png')],check=True)
    panel=Image.new('RGB',(960,300),'#122638');d=ImageDraw.Draw(panel);d.text((12,5),f'{t}s ORIGINAL',font=font,fill='white');d.text((492,5),'REMOTION',font=font,fill='white')
    panel.paste(Image.open(root/f'original-{t}.png').resize((480,270)),(0,30));panel.paste(Image.open(root/f'frame-{t}.png').resize((480,270)),(480,30));contact.paste(panel,((i%2)*960,(i//2)*300))
contact.save(root/'reference-comparison.png')
