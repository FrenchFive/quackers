from PIL import Image, ImageDraw, ImageFont
import os
import requests

SCRPTDIR = os.path.dirname(os.path.abspath(__file__))
IMGFOLDER = os.path.join(SCRPTDIR, "imgs")
WOSKER = os.path.join(IMGFOLDER, 'fonts/thunder.ttf')
SCHABO = os.path.join(IMGFOLDER, 'fonts/schabo.otf')

def info(name, url, result, rank):
    name = name[:20].upper() #CUTTING THE NAME

    coins = result[0]
    mess = result[1]
    date = result[2]
    date = date[:10]
    voice = result[3]
    voiceh = result[4]
    luck = result[5]

    # Create a base image
    GLBDIM = (3800, 1000)
    base = Image.new('RGBA', GLBDIM, (255, 255, 255, 255))

    #DOWNLOAD USER AVATAR
    img_data = requests.get(url).content
    tmpavatar = os.path.join(IMGFOLDER, "tmpuser.jpg")
    with open(tmpavatar, 'wb') as handler:
        handler.write(img_data)
    
    #AVATAR
    avatar = Image.open(tmpavatar).convert('RGB')
    lildim = 900
    dim = (lildim, lildim)
    center = (lildim/2, lildim/2)
    avatar = avatar.resize(dim)
    mask = Image.new('L', dim, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, dim[0], dim[1]), fill=255)
    if voice != 0:
        radius = 90
        tmpcenter = (300,300)
        draw.ellipse((radius, radius, tmpcenter[0]-radius, tmpcenter[1]-radius), fill=0)
    mask.save(os.path.join(IMGFOLDER, "tmp.png"))
    rest = int((GLBDIM[1] - dim[1])/2)
    base.paste(avatar, (rest, rest), mask)
    #GREEN CIRCLE IF CONNECTED TO A VOICE CHANNEL
    if voice != 0:
        mask = Image.new('RGBA', dim, 0)
        draw = ImageDraw.Draw(mask)
        radius = 100
        draw.ellipse((radius, radius, tmpcenter[0]-radius, tmpcenter[1]-radius), fill="green")
        base.paste(mask, (rest, rest), mask)
    

    #DISPLAY NAME
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(WOSKER, size=400)
    draw.text(((rest*2)+lildim, rest*2), name, fill=(0, 0, 0, 255), font=font)

    #BIG INFO
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(SCHABO, size=180)  # You can specify your custom font
    text = f"{coins} Quack Coins"
    draw.text(((rest*2)+lildim + 15, rest*2 + 440), text, fill=(0, 0, 0, 255), font=font)

    #SMALLER INFO
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(SCHABO, size=120)  # You can specify your custom font
    text = f"MESSAGES : {mess} // VC HOURS : {voiceh} // LUCK : {luck}"
    draw.text(((rest*2)+lildim + 15, rest*2 + 610), text, fill=(0, 0, 0, 255), font=font)

    #MEMBER SINCE
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(SCHABO, size=120)
    text = f"MEMBER SINCE : {date}"
    draw.text(((rest*2)+lildim + 15, rest*2 + 725), text, fill=(0, 0, 0, 255), font=font)

    #RANK
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(SCHABO, size=400)  # You can specify your custom font
    text = f"#{str(rank).zfill(3)}"
    draw.text((GLBDIM[0]-700,GLBDIM[1]-340), text, fill=(0, 0, 0, 255), font=font)

    #FINALLY SAVE
    final = os.path.join(IMGFOLDER, "final.png")
    base.save(final)
    return(final)
