# rank image creation go brrrr
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
import shutil

# create width and height for ranked image
W, H = 250, 250
w, h = 0, 25

#import and create fonts
DisiFont15 = ImageFont.truetype("src/fonts/font.ttf", 15)
DisiFont20 = ImageFont.truetype("src/fonts/font.ttf", 20)

def RankImage_DownloadBadges(Rank, Arena):
    # download BR rank image and store it
    RankImgRequest = requests.get(Rank['rankImg'], allow_redirects=True, stream=True)
    with open('src/rank/' + Rank['rankName'] + str(Rank['rankDiv']) + '.png','wb') as f:
        shutil.copyfileobj(RankImgRequest.raw, f)

    # download AR rank image and store it
    RankImgRequest = requests.get(Arena['rankImg'], allow_redirects=True, stream=True)
    with open('src/rank/' + Arena['rankName'] + str(Arena['rankDiv']) + '.png','wb') as f:
        shutil.copyfileobj(RankImgRequest.raw, f)

def RankImage_Create():
    #create new image
    global img
    img = Image.new('RGBA', (W, H))
    global img1draw
    img1draw = ImageDraw.Draw(img)

def RankImage_PlayerName(Name):
    # write player name text
    FontSize = 25
    w = W + 1
    while w > W:
        NameFont = ImageFont.truetype("src/fonts/font.ttf", FontSize)
        w, h = img1draw.textsize(Name, font=NameFont)
        if FontSize == 10:
            break
        FontSize -= 1
    img1draw.text(((W - w) / 2, 0), Name, fill="white", font=NameFont)

def RankImage_BRbadge(Rank):
    # write BR Rank text
    w1, h1 = img1draw.textsize('BR Rank', font=DisiFont20)
    img1draw.text((((W / 2) - w1) / 2, h + 10), 'BR Rank', fill='white', font=DisiFont20)

    # draw BR Rank symbol
    imgrank = Image.open('src/rank/' + Rank['rankName'] + str(Rank['rankDiv']) + '.png')
    imgrank = imgrank.resize((120, 120), Image.ADAPTIVE)
    area = (int(((W / 2) - 120) / 2), h + h1 + 20, int(((W / 2) - 120) / 2) + 120, h + h1 + 140)
    img.paste(imgrank, area)
    imgrank.close()

    # check if predator badge was placed
    if 'Apex Predator' == Rank['rankName']:
        # write Predator rank
        w2, h2 = img1draw.textsize('#' + str(Rank['ladderPosPlatform']), font=DisiFont15)
        img1draw.text(((((W / 2) - w2) / 2), h + h1 + 113), '#' + str(Rank['ladderPosPlatform']), fill='white', font=DisiFont15)
    
    # write BR Rank value
    w1, h1 = img1draw.textsize(str(Rank['rankScore']) + 'RP', font=DisiFont20)
    img1draw.text((((W / 2) - w1) / 2, h + h1 + 150), str(Rank['rankScore']) + 'RP', fill='white', font=DisiFont20)

def RankImage_ARbadge(Arena):
    # write AR Rank text
    w1, h1 = img1draw.textsize('AR Rank', font=DisiFont20)
    img1draw.text(((((W / 2) - w1) / 2) + (W / 2), h + 10), 'AR Rank', fill='white', font=DisiFont20)

    # draw AR Rank symbol
    imgrank = Image.open('src/rank/' + Arena['rankName'] + str(Arena['rankDiv']) + '.png')
    imgrank = imgrank.resize((120, 120), Image.ADAPTIVE)
    area = (int(((W / 2) - 120) / 2 + (W / 2)), h + h1 + 20, int(((W / 2) - 120) / 2 + (W / 2)) + 120, h + h1 + 140)
    img.paste(imgrank, area)
    imgrank.close()

    # check if predator badge was placed
    if 'Apex Predator' == Arena['rankName']:
        # write Predator rank
        w2, h2 = img1draw.textsize('#' + str(Arena['ladderPosPlatform']), font=DisiFont15)
        img1draw.text(((((W / 2) - w2) / 2) + (W / 2), h + h1 + 113), '#' + str(Arena['ladderPosPlatform']), fill='white', font=DisiFont15)

    # write AR Rank value
    w1, h1 = img1draw.textsize(str(Arena['rankScore']) + 'AP', font=DisiFont20)
    img1draw.text(((((W / 2) - w1) / 2) + (W / 2), h + h1 + 150), str(Arena['rankScore']) + 'AP', fill='white', font=DisiFont20)

def RankImage_Save():
     # save picture
    img.save('src/rank/rank.png')
    img.close()