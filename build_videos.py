#!/usr/bin/env python3
"""OUT OF ORDER — TikTok verdict video builder.
Renders 1080x1920 vertical MP4s from the judge audio + evidence photos.
Usage: python3 build_videos.py
"""
import os, subprocess, math, shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT='/home/user/out-of-order'
TMP='/tmp/oo_frames'
OUT=os.path.join(ROOT,'tiktok')
FFMPEG=subprocess.check_output(['python3','-c','import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())']).decode().strip()

W,H=1080,1920
F_SER ='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
F_SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F_MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
INK=(22,19,15); INK2=(58,51,42); PAPER=(242,234,216); GOLD=(212,175,55); BRASS=(138,109,31)
RED=(148,34,27); DRED=(110,24,18); CREAM=(239,230,207); WHITE=(255,252,244)

def F(p,s): return ImageFont.truetype(p,s)
def wrap(draw,text,f,maxw):
    out=[]
    for para in text.split('\n'):
        line=''
        for word in para.split(' '):
            test=(line+' '+word).strip()
            if draw.textlength(test,font=f)<=maxw: line=test
            else: out.append(line); line=word
        out.append(line)
    return out
def ctext(draw,cx,y,lines,f,fill,stroke=0,sfill=(0,0,0)):
    for ln in lines:
        draw.text((cx,y),ln,font=f,fill=fill,anchor='ma',stroke_width=stroke,stroke_fill=sfill)
        y+=f.size*1.32
    return y
def chip(draw,cx,y,text,f,bg,fg,padx=26,pady=14):
    w=draw.textlength(text,font=f)+padx*2; h=f.size+pady*2
    draw.rectangle([cx-w/2,y,cx+w/2,y+h],fill=bg)
    draw.text((cx,y+h/2),text,font=f,fill=fg,anchor='mm')
    return h

def brand_top(draw,mono24,color):
    draw.line([(60,210),(W-60,210)],fill=BRASS,width=2)
    draw.text((W/2,238),'OUT OF ORDER · COURT OF PETTY DISPUTES',font=mono24,fill=color,anchor='ma')

def judge_circle(img_draw_img,size,ring=10):
    j=Image.open(os.path.join(ROOT,'images','judge-avatar.png')).convert('RGB')
    j=ImageOps.fit(j,(size,size))
    mask=Image.new('L',(size,size),0); ImageDraw.Draw(mask).ellipse([0,0,size,size],fill=255)
    out=Image.new('RGBA',(size+ring*2,size+ring*2),(0,0,0,0))
    d=ImageDraw.Draw(out); d.ellipse([0,0,size+ring*2,size+ring*2],fill=GOLD)
    d.ellipse([ring-4,ring-4,size+ring+4,size+ring+4],fill=BRASS)
    out.paste(j,(ring,ring),mask)
    return out

def make_hook(c,frames_dir):
    ph=Image.open(os.path.join(ROOT,'images',c['img'])).convert('RGB')
    bg=ImageOps.fit(ph,(W,H))
    grad=Image.new('L',(1,H))
    for y in range(H):
        a=0 if y<H*0.42 else int(((y/H)-0.42)/0.58*215)
        grad.putpixel((0,y),a)
    bg.paste((0,0,0),(0,0),grad.resize((W,H)))
    d=ImageDraw.Draw(bg)
    mono28=F(F_MONO,28); ser64=F(F_SER,64)
    draw=d
    chip(draw,W/2,225,'EXHIBIT A',F(F_MONO,34),GOLD,INK)
    draw.text((W/2,332),f"CASE {c['no']} · NOW ARRAIGNING",font=mono28,fill=CREAM,anchor='ma',stroke_width=2,stroke_fill=(0,0,0))
    lines=wrap(draw,c['hook'],ser64,900)
    block=len(lines)*ser64.size*1.32
    ctext(draw,W/2,int(H-360-block),lines,ser64,WHITE,stroke=3)
    draw.text((W/2,H-250),'THE RULING, NEXT  >>',font=F(F_MONO,30),fill=GOLD,anchor='ma')
    p=os.path.join(frames_dir,'hook.png'); bg.save(p); return p

def make_cap(c,frames_dir,idx,total):
    bg=Image.new('RGB',(W,H),INK); d=ImageDraw.Draw(bg)
    mono24=F(F_MONO,24); mono26=F(F_MONO,26)
    brand_top(d,mono24,GOLD)
    d.rectangle([60,300,60+8+d.textlength(c['no'].upper(),font=F(F_SANS,30))+40,352],fill=PAPER)
    d.text((60+28,326),c['no'].upper(),font=F(F_SANS,30),fill=INK,anchor='lm')
    d.text((W-60,326),'● LIVE VERDICT',font=F(F_SANS,28),fill=(226,88,74),anchor='rm')
    jc=judge_circle(d,320,9); bg.paste(jc,((W-jc.width)//2,400),jc)
    d.text((W/2,790),'JUDGE RONALD WAPNER III',font=mono24,fill=BRASS,anchor='ma')
    seg_w,gap,y=280,14,834
    x0=W/2-(total*seg_w+(total-1)*gap)/2
    for i in range(total):
        d.rectangle([x0+i*(seg_w+gap),y,x0+i*(seg_w+gap)+seg_w,y+9],
                    fill=GOLD if i<idx else (58,51,42))
    lines=wrap(d,c['caps'][idx-1],F(F_SER,58),860)
    ctext(d,W/2,1010,lines,F(F_SER,58),CREAM)
    d.text((W/2,1500),'VERDICT READ INTO RECORD',font=mono26,fill=GOLD,anchor='ma')
    p=os.path.join(frames_dir,f'cap{idx}.png'); bg.save(p); return p

def make_stamp(c,frames_dir):
    bg=Image.new('RGB',(W,H),DRED); d=ImageDraw.Draw(bg)
    d.rectangle([36,36,W-36,H-36],outline=CREAM,width=8)
    d.rectangle([58,58,W-58,H-58],outline=CREAM,width=3)
    layer=Image.new('RGBA',(W,500),(0,0,0,0)); ld=ImageDraw.Draw(layer)
    txt='GUILTY'
    f=F(F_SER,190)
    w=ld.textlength(txt,font=f)
    ld.rectangle([W/2-w/2-56,110,W/2+w/2+56,110+300],outline=WHITE,width=10)
    ld.rectangle([W/2-w/2-38,128,W/2+w/2+38,128+264],outline=WHITE,width=3)
    ld.text((W/2,128+132),txt,font=f,fill=WHITE,anchor='mm')
    layer=layer.rotate(-8,expand=True,resample=Image.BICUBIC)
    bg.paste(layer,(int(W/2-layer.width/2),470),layer)
    y=ctext(d,W/2,1010,wrap(d,c['order'],F(F_MONO,32),820),F(F_MONO,32),CREAM)
    ctext(d,W/2,y+90,[f"CASE {c['no']} · ADJUDGED IN OPEN COURT"],F(F_MONO,24),(240,205,200))
    p=os.path.join(frames_dir,'stamp.png'); bg.save(p); return p

def make_cta(c,frames_dir):
    bg=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(bg)
    mono24=F(F_MONO,24)
    brand_top(d,mono24,BRASS)
    seal=Image.new('RGBA',(340,340),(0,0,0,0)); sd=ImageDraw.Draw(seal)
    sd.ellipse([0,0,340,340],fill=GOLD); sd.ellipse([12,12,328,328],fill=BRASS); sd.ellipse([20,20,320,320],fill=GOLD)
    sd.ellipse([34,34,306,306],fill=INK)
    sd.text((170,158),'§',font=F(F_SER,150),fill=GOLD,anchor='mm')
    bg.paste(seal,((W-340)//2,330),seal)
    d.text((W/2,760),'SUE SOMEONE — $3',font=F(F_SER,80),fill=INK,anchor='ma')
    for i,t in enumerate(['Judge verdicts: FREE','The public jury: $5','The accused pays $3 to respond.']):
        d.text((W/2,900+i*64),t,font=F(F_SANS,40),fill=INK2,anchor='ma')
    url='petty-court.github.io/Out-of-order/'
    fu=F(F_MONO,38); wu=d.textlength(url,font=fu)
    d.rectangle([W/2-wu/2-40,1160,W/2+wu/2+40,1160+88],fill=INK)
    d.text((W/2,1160+44),url,font=fu,fill=GOLD,anchor='mm')
    d.text((W/2,1330),'LINK IN BIO — JUSTICE WITHIN 24 HOURS',font=mono24,fill=BRASS,anchor='ma')
    d.text((W/2,H-240),'OUT OF ORDER · PARODY COURT · NOT LEGAL ADVICE (OBVIOUSLY)',font=F(F_MONO,20),fill=(122,108,72),anchor='ma')
    p=os.path.join(frames_dir,'cta.png'); bg.save(p); return p

CASES=[
 {'id':'0047','no':'#0047','img':'ryan.jpg','audio':'verdict-0047.mp3','dur':25.18,
  'hook':"He owed her $7 for the Uber.\nFOUR days of “I'll send it.”\nSo she took him to internet court.",
  'caps':["The court has reviewed Exhibit A: a payment request ignored for four days.",
          "Mr. Ryan was “about to send it.” Mr. Ryan was at the golf club. Posting.",
          "The court finds FOR THE PLAINTIFF. Pay the fare, plus a three-word apology. No emojis."],
  'order':'ORDERED: PAY $7 + A 3-WORD APOLOGY.\nNO EMOJIS.'},
 {'id':'0052','no':'#0052','img':'cat.jpg','audio':'verdict-0052.mp3','dur':24.62,
  'hook':"She caught her cat\neating her tuna. The can,\nhe claims, “opened itself.”",
  'caps':["The defendant, a known tuna enthusiast, was found at the scene wearing the tuna.",
          "The defense — “the can opened itself” — has been rejected by physics.",
          "Guilty. Sentence: immediate belly rubs, reduced to time served. The court is not a monster."],
  'order':'ORDERED: BELLY RUBS.\nREDUCED TO TIME SERVED.'},
 {'id':'0093','no':'#0093','img':'dave.jpg','audio':'verdict-0093.mp3','dur':24.82,
  'hook':"He declared Die Hard\nis not a Christmas movie.\nThe internet's court took that personally.",
  'caps':["The defendant argued, publicly and without shame, that Die Hard is not a Christmas movie.",
          "The evidence: snow. An office Christmas party. Alan Rickman in a suit.",
          "Take it down, Dave. Post a retraction. Apologize to the group chat. The court finds for Christmas."],
  'order':'ORDERED: DELETE THE TAKE.\nAPOLOGIZE TO THE GROUP CHAT.'},
]

HOOK_T, STAMP_T, CTA_T = 2.6, 1.5, 2.8

def seg_encode(png,dur,rate,outp):
    frames=int(dur*30)+2
    vf=(f"scale=1920:3413,zoompan=z='1+{rate}*in':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={frames}:s=1080x1920:fps=30,format=yuv420p")
    subprocess.run([FFMPEG,'-y','-loop','1','-framerate','30','-t',str(dur),'-i',png,
        '-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','20','-t',str(dur),outp],
        check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def build(c):
    fd=os.path.join(TMP,c['id']); shutil.rmtree(fd,ignore_errors=True); os.makedirs(fd)
    segs=[(make_hook(c,fd),HOOK_T,0.0022)]
    total_chars=sum(len(x) for x in c['caps'])
    acc=0.0; ts=[]
    for i,txt in enumerate(c['caps']):
        d=max(3.2, c['dur']*len(txt)/total_chars)
        acc+=d; ts.append(d)
    ts[-1]+= c['dur']-acc  # fix rounding on last segment
    for i in range(3):
        segs.append((make_cap(c,fd,i+1,3),ts[i],0.0008))
    segs.append((make_stamp(c,fd),STAMP_T,0.0004))
    segs.append((make_cta(c,fd),CTA_T,0.0006))
    parts=[]
    for i,(png,dur,rate) in enumerate(segs):
        op=os.path.join(fd,f'seg{i}.mp4'); seg_encode(png,dur,rate,op); parts.append(op)
    lst=os.path.join(fd,'list.txt')
    with open(lst,'w') as f:
        for p in parts: f.write(f"file '{p}'\n")
    vonly=os.path.join(fd,'video.mp4')
    subprocess.run([FFMPEG,'-y','-f','concat','-safe','0','-i',lst,'-c','copy',vonly],
        check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    total=sum(d for _,d,_ in segs)
    hook_ms=int(HOOK_T*1000); boom_ms=int((HOOK_T+c['dur'])*1000)
    audio=os.path.join(ROOT,'audio',c['audio'])
    out=os.path.join(OUT,f"tiktok-{c['id']}.mp4")
    fc=(f"[1:a]adelay={hook_ms}|{hook_ms},apad,aformat=channel_layouts=stereo[a1];"
        f"[2:a]volume=2.4,adelay={boom_ms}|{boom_ms},aformat=channel_layouts=stereo[b];"
        f"[3:a][a1][b]amix=inputs=3:normalize=0[mix]")
    subprocess.run([FFMPEG,'-y','-i',vonly,'-i',audio,
        '-f','lavfi','-t','0.6','-i','sine=frequency=55:sample_rate=44100',
        '-f','lavfi','-i','anullsrc=r=44100:cl=stereo',
        '-filter_complex',fc,'-map','0:v','-map','[mix]',
        '-c:v','copy','-c:a','aac','-b:a','128k','-t',f'{total:.2f}',out],
        check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(f"  OK {out} ({total:.1f}s, {os.path.getsize(out)//1024} KB)")
    shutil.rmtree(fd,ignore_errors=True)

os.makedirs(OUT,exist_ok=True); os.makedirs(TMP,exist_ok=True)
for c in CASES:
    print('rendering case',c['id'],'…'); build(c)
shutil.rmtree(TMP,ignore_errors=True)
print('ALL VIDEOS DONE')
