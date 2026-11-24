# Rebuilds images/hero-logo-*.webp. Inputs: logo-source.jpg (client logo, 1254px) and cut/*.png,
# made from the Pexels photos 8524618, 6606139, 7294852 with: swift hero_cutout.swift big/ID.jpg cut/ID.png
# Run from a scratch folder holding those files.
from PIL import Image, ImageDraw, ImageFilter
W,H=1100,1375; SS=2
bg=Image.new('RGBA',(W,H),(250,247,253,255))
# board
board=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(board)
bx0,by0,bx1,by1=60,60,1040,870
sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((bx0,by0+18,bx1,by1+18),40,fill=(34,10,85,60)); sh=sh.filter(ImageFilter.GaussianBlur(28))
bg.alpha_composite(sh)
d.rounded_rectangle((bx0,by0,bx1,by1),40,fill=(240,232,250,255),outline=(225,212,243,255),width=3)
bg.alpha_composite(board)
# logo badge (antialiased circle)
src=Image.open('logo-source.jpg').convert('RGBA'); cx,cy,r=624,601,551
logo=src.crop((cx-r,cy-r,cx+r,cy+r)); D=530; LX=660; LY=80
m=Image.new('L',(2*r*4,2*r*4),0); ImageDraw.Draw(m).ellipse((0,0,2*r*4-1,2*r*4-1),fill=255); m=m.resize((2*r,2*r),Image.LANCZOS)
logo.putalpha(m); logo=logo.resize((D,D),Image.LANCZOS)
ls=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(ls).ellipse((LX-D//2,LY+16,LX+D//2,LY+D+16),fill=(34,10,85,70)); ls=ls.filter(ImageFilter.GaussianBlur(22)); bg.alpha_composite(ls)
bg.alpha_composite(logo,(LX-D//2,LY))
# people: (file, height, x-centre)
ground=1290
people=[("cut/8524618.png",590,255),("cut/6606139.png",615,555),("cut/7294852.png",630,848)]
for f,h,xc in people:
    p=Image.open(f).convert('RGBA'); w=int(p.width*h/p.height); p=p.resize((w,h),Image.LANCZOS)
    s=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(s).ellipse((xc-w*0.46,ground-22,xc+w*0.46,ground+14),fill=(34,10,85,70)); s=s.filter(ImageFilter.GaussianBlur(14)); bg.alpha_composite(s)
    bg.alpha_composite(p,(int(xc-w/2),ground-h))
bg.convert('RGB').save('hero-new.png')
print('ok')
