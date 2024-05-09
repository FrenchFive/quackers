from PIL import Image, ImageDraw, ImageFont
import os
import requests

SCRPTDIR = os.path.dirname(os.path.abspath(__file__))
IMGFOLDER = os.path.join(SCRPTDIR, "imgs")
WOSKER = os.path.join(IMGFOLDER, 'fonts/wosker.otf')
SCHABO = os.path.join(IMGFOLDER, 'fonts/schabo.otf')

def info(name, url, result):
    name = name[:12].upper() #CUTTING THE NAME

    coin = result[0]
    mess = result[1]
    date = result[2]
    date = date[:10]
    voice = result[3]
    rank = 5

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
    avatar = avatar.resize(dim)
    mask = Image.new('L', dim, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, dim[0], dim[1]), fill=255)
    rest = int((GLBDIM[1] - dim[1])/2)
    base.paste(avatar, (rest, rest), mask)
    #GREEN CIRCLE IF CONNECTED TO A VOICE CHANNEL
    if voice != 0:
        draw = ImageDraw.Draw(base)
        center = (180, 180)  # Center coordinates of the circle
        radius = 70  # Radius of the circle
        draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill="green")

    #DISPLAY NAME
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(WOSKER, size=350)
    draw.text(((rest*2)+lildim, rest*2), name, fill=(0, 0, 0, 255), font=font)

    #FINALLY SAVE
    final = os.path.join(IMGFOLDER, "final.png")
    base.save(final)

info("quack_five", "https://cdn.discordapp.com/avatars/475985107241402368/ef1b0f90c431ac30620100545c99ed96.png?size=1024", (7773, 518, '2024-04-05 19:44', 1715286216))
