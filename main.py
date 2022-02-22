# much epic disi apex bot go brrrrrrrrrrrrrrrrrrrrrrrrrr
import os
import sys
from typing import Counter
#from urllib import response
import discord
from discord.ext import commands
import json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
import shutil
import urllib.request

#import and create fonts
DisiFont20 = ImageFont.truetype("font.ttf", 20)
DisiFont25 = ImageFont.truetype("font.ttf", 25)

# get discord api key form file
DISI_TOKEN_FILE = open("src/token/DISI_API_TOKEN", 'r')
DISI_TOKEN = DISI_TOKEN_FILE.read()
DISI_TOKEN_FILE.close()

# get apex api key form file
APEX_TOKEN_FILE = open("src/token/APEX_API_TOKEN", 'r')
APEX_TOKEN = APEX_TOKEN_FILE.read()
APEX_TOKEN_FILE.close()

# create bot with a command prefix
client = commands.Bot(command_prefix="!")

# on ready event for start of bot
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@client.command()
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def pingall(ctx):
    await ctx.channel.send('@everyone')
    await ctx.channel.send(file=discord.File('src/ping.jpg'))

@client.command()
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def map(ctx):
    # send request to the api and store the response
    RequestForMaps = requests.get('https://api.mozambiquehe.re/maprotation?version=2&auth=' + APEX_TOKEN)
    RequestDataResponse = RequestForMaps.json()

    # choose right image for map
    if RequestDataResponse['battle_royale']['current']['map'] == 'Olympus': # map is opympus
        await ctx.channel.send(file=discord.File('src/maps/olympus.jpg'))

    elif RequestDataResponse['battle_royale']['current']['map'] == 'Kings Canyon': # map is kings canyon
        await ctx.channel.send(file=discord.File('src/maps/kings-canyon.jpg'))

    elif RequestDataResponse['battle_royale']['current']['map'] == 'Storm Point': # map is storm point
        await ctx.channel.send(file=discord.File('src/maps/stormpoint.jpg'))

    else: #default case
        await ctx.channel.send('```diff' +
                                'Map image not implemented yet.'
                                '```')
    

    # send battle royale maps
    await ctx.channel.send('**BATTLE ROYALE**' + 
                                '\n```Current map: ' + RequestDataResponse['battle_royale']['current']['map'] +
                                '\nRemaining: ' + RequestDataResponse['battle_royale']['current']['remainingTimer'] +
                                '\nNext map: ' + RequestDataResponse['battle_royale']['next']['map'] +
                                '```')

    #send battle royale ranked map
    await ctx.channel.send('**BATTLE ROYALE RANKED**' +
                                '\n```Current map: ' + RequestDataResponse['ranked']['current']['map'] +
                                '\nNext split map: ' + RequestDataResponse['ranked']['next']['map'] +
                                '```')

    #send arenas maps
    await ctx.channel.send('**ARENAS**' +
                                '\n```Current map: ' + RequestDataResponse['arenas']['current']['map'] +
                                '\nRemaining: ' + RequestDataResponse['arenas']['current']['remainingTimer'] +
                                '\nNext map: ' + RequestDataResponse['arenas']['next']['map'] +
                                '```')

    #send arenas ranked maps
    await ctx.channel.send('**ARENAS RANKED**' +
                                '\n```Current map: ' + RequestDataResponse['arenasRanked']['current']['map'] +
                                '\nRemaining: ' + RequestDataResponse['arenasRanked']['current']['remainingTimer'] +
                                ' \nNext map: ' + RequestDataResponse['arenasRanked']['next']['map'] +
                                '```')

@client.command()
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def stats(ctx, arg):
    # create variables
    PlayerFound, CounterForFor, Platforms = 0, 0, ['PC', 'PS4', 'X1']

    while PlayerFound == 0:
        # check if all the platforms have been checked
        if CounterForFor >= 3:
            # goto error and break
            PlayerFound = 2
            break

        # send request to the api and store the response
        RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=' + Platforms[CounterForFor] + '&player=' + arg + '&auth=' + APEX_TOKEN)
        RequestDataResponse = json.loads(RequestForStats.text)

        # check if the api sent a error
        if 'Error' in RequestDataResponse: 
            PlayerFound = 0
        elif 'global' in RequestDataResponse:
            PlayerFound = 1

        CounterForFor += 1
        

    if PlayerFound == 1: # Player exists in database
        # send name and current legend to discord
        await ctx.channel.send('**' + RequestDataResponse['global']['name'] + '**`s' + ' current Legend is **' + RequestDataResponse['legends']['selected']['LegendName'] + '**')
        
        # download banner image and store it
        BannerImgRequest = requests.get(str(RequestDataResponse['legends']['selected']['ImgAssets']['banner']), allow_redirects=True)
        open('src/banners/' + RequestDataResponse['legends']['selected']['LegendName'] + '.jpg', 'wb').write(BannerImgRequest.content)

        # send banner image to discord
        await ctx.channel.send(file=discord.File('src/banners/' + RequestDataResponse['legends']['selected']['LegendName'] + '.jpg'))

        # change X1 platform to Xbox 1 of needed
        RequestDataResponse['global']['platform'] = RequestDataResponse['global']['platform'].replace('X1', 'Xbox 1')

        #send data as one package
        await ctx.channel.send('**Platform: ' + RequestDataResponse['global']['platform'] + '**\n'
                                '**Level: ' + str(RequestDataResponse['global']['level']) + '**\n' +
                                '**Status: ' + str(RequestDataResponse['realtime']['currentStateAsText']) + '**\n_ _')

        # check if there are any trackers equiped
        if 'data' in RequestDataResponse['legends']['selected']:
            name = 'name'
            # set the messages for trackers to default
            messageTracker = ['no data', 'no data', 'no data']

            CounterForFor = 0
            
            # loop for every tracker equiped
            for name in RequestDataResponse['legends']['selected']['data']: 
                if 'name' in RequestDataResponse['legends']['selected']['data'][CounterForFor]:
                    messageTracker[CounterForFor] = RequestDataResponse['legends']['selected']['data'][CounterForFor]['name'] + ': ' + str(RequestDataResponse['legends']['selected']['data'][CounterForFor]['value'])
                    messageTracker[CounterForFor] = messageTracker[CounterForFor].replace('Special event ', '')
                    messageTracker[CounterForFor] = messageTracker[CounterForFor].capitalize()

                CounterForFor += 1
        
        # send tracker message as a package        
        await ctx.channel.send('**Trackers: **\n' +
                                    '```' + messageTracker[0] + '\n' +
                                    messageTracker[1] + '\n' +
                                    messageTracker[2] + '```')

    elif PlayerFound == 2: # player not found or error
        # send error message to discord channel
        await ctx.channel.send(RequestDataResponse['Error'])
        await ctx.channel.send(file=discord.File('src/sad-cute.gif'))
        # print error message to cli
        print('Error during request to API, message from API: ' + str(RequestDataResponse))

@client.command()
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def rank(ctx, arg):
    RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=PC&player=' + arg + '&auth=' + APEX_TOKEN)
    RequestDataResponse = json.loads(RequestForStats.text)

    if 'Error' in RequestDataResponse:
        # send error message to discord channel
        await ctx.channel.send(RequestDataResponse['Error'])
        await ctx.channel.send(file=discord.File('src/sad-cute.gif'))
        # print error message to cli
        print('Error during request to API, message from API: ' + str(RequestDataResponse))

    else:
        W, H = 250, 250
        img = Image.new("RGBA", (W, H))
        img1draw = ImageDraw.Draw(img)

        w, h = img1draw.textsize(RequestDataResponse['global']['name'], font=DisiFont25)
        img1draw.text(((W - w) / 2, 0), RequestDataResponse['global']['name'], fill="white", font=DisiFont25)

        w1, h1 = img1draw.textsize("BR Rank", font=DisiFont20)
        img1draw.text((((W / 2) - w1) / 2, h + 20), "BR Rank", fill="white", font=DisiFont20)

        filename = "rank.png"
        r = requests.get(RequestDataResponse['global']['rank']['rankImg'], stream = True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
        imgrank = Image.open(filename)
        img.paste(imgrank, (int(((W / 2) - 120) / 2), h + h1 + 40))

        w1, h1 = img1draw.textsize("Arena Rank", font=DisiFont20)
        img1draw.text(((((W / 2) - w1) / 2) + (W / 2), h + 20), "Arena Rank", fill="white", font=DisiFont20)

        r = requests.get(RequestDataResponse['global']['arena']['rankImg'], stream = True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
        imgrank = Image.open(filename)
        img.paste(imgrank, (int(((W / 2) - 120) / 2 + (W / 2)), h + h1 + 40))

        w, h = img1draw.textsize(str(RequestDataResponse['global']['rank']['rankScore']) + 'RP', font=DisiFont20)
        img1draw.text((((W / 2) - w) / 2, (H - h) - 20), str(RequestDataResponse['global']['rank']['rankScore']) + 'RP', fill="white", font=DisiFont20)

        w, h = img1draw.textsize(str(RequestDataResponse['global']['arena']['rankScore']) + 'AP', font=DisiFont20)
        img1draw.text(((((W / 2) - w) / 2) + (W / 2), (H - h) - 20), str(RequestDataResponse['global']['arena']['rankScore']) + 'AP', fill="white", font=DisiFont20)

        img.save('output.png')

        await ctx.channel.send(file=discord.File('output.png'))

# run the client
client.run(DISI_TOKEN)

