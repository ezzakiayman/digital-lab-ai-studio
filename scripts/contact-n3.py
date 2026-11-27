from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
p=json.loads(Path('src/video/n3-plan.json').read_text(encoding='utf-8'));files=[(s,Path('outputs/n3')/(s['id']+'.png')) for s in p['scenes']];files=[x for x in files if x[1].exists()]
out=Image.new('RGB',(1440,300*math.ceil(len(files)/3)),'#122638');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for i,(s,f) in enumerate(files):
 x=(i%3)*480;y=(i//3)*300;out.paste(Image.open(f).resize((480,270)),(x,y+30));ImageDraw.Draw(out).text((x+10,y+6),s['id'],font=font,fill='white')
out.save('outputs/n3/storyboard-preview.png')
