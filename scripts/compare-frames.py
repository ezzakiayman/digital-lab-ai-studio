from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageEnhance
from pathlib import Path
root=Path('outputs/comparison');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
sheet=Image.new('RGB',(1920,588*3),'#122638')
for row,second in enumerate([14,27,36]):
    a=Image.open(root/f'original-{second}.png').convert('RGB');b=Image.open(root/f'generated-{second}.png').convert('RGB')
    panel=Image.new('RGB',(1920,588),'#122638');d=ImageDraw.Draw(panel)
    d.text((20,12),f'ORIGINAL | {58+second}.00 s',font=font,fill='white');d.text((980,12),f'REMOTION | {second}.00 s',font=font,fill='white')
    panel.paste(a.resize((960,540)),(0,48));panel.paste(b.resize((960,540)),(960,48));panel.save(root/f'side-by-side-{second}.png');sheet.paste(panel,(0,row*588))
    ImageEnhance.Contrast(ImageChops.difference(a,b)).enhance(4).save(root/f'difference-{second}.png')
sheet.save(root/'comparison-contact.png')

