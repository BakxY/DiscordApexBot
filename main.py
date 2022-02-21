# much epic disi apex bot go brrrrrrrrrrrrrrrrrrrrrrrrrr
import os
import sys
from urllib import response
import discord
from dotenv import load_dotenv
from apex_legends_api import ApexLegendsAPI,\
    ALPlatform,\
    ALPlayer,\
    ALAction,\
    ALHTTPExceptionFromResponse
from apex_legends_api.al_base import print_description
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
import shutil

DisiFont20 = ImageFont.truetype("font.ttf", 20)
DisiFont25 = ImageFont.truetype("font.ttf", 25)

load_dotenv()

# get discord api key form file
DISI_TOKEN_FILE = open("DISI_API_TOKEN", 'r')
DISI_TOKEN = DISI_TOKEN_FILE.read()
DISI_TOKEN_FILE.close()

#create a new discord client object
client = discord.Client()

# get apex api key form file
APEX_TOKEN_FILE = open("APEX_API_TOKEN", 'r')
APEX_TOKEN = APEX_TOKEN_FILE.read()
APEX_API = ApexLegendsAPI(APEX_TOKEN)
APEX_TOKEN_FILE.close()

RequestDataResponse = ''

# on ready event for start of bot
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

# on message for any sent messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!ping all':
        await message.channel.send('@everyone')
        await message.channel.send(file=discord.File('ping.jpg'))

    if message.content == '!map':
        RequestForMaps = requests.get('https://api.mozambiquehe.re/maprotation?version=2&auth=' + APEX_TOKEN)
        RequestDataResponse = json.loads(RequestForMaps.text)

        if RequestDataResponse['battle_royale']['current']['map'] == 'Olympus':
            await message.channel.send(file=discord.File('olympus.jpg'))

        if RequestDataResponse['battle_royale']['current']['map'] == 'Kings Canyon':
            await message.channel.send(file=discord.File('kings-canyon.jpg'))

        if RequestDataResponse['battle_royale']['current']['map'] == 'Storm Point':
            await message.channel.send(file=discord.File('stormpoint.jpg'))

        # send battle royale maps
        await message.channel.send('**BATTLE ROYALE**' + 
                                    '\n```Current map: ' + RequestDataResponse['battle_royale']['current']['map'] +
                                    '\nRemaining: ' + RequestDataResponse['battle_royale']['current']['remainingTimer'] +
                                    '\nNext map: ' + RequestDataResponse['battle_royale']['next']['map'] +
                                    '```')

        #send battle royale ranked map
        await message.channel.send('**BATTLE ROYALE RANKED**' +
                                    '\n```Current map: ' + RequestDataResponse['ranked']['current']['map'] +
                                    '\nNext split map: ' + RequestDataResponse['ranked']['next']['map'] +
                                    '```')

        #send arenas maps
        await message.channel.send('**ARENAS**' +
                                    '\n```Current map: ' + RequestDataResponse['arenas']['current']['map'] +
                                    '\nRemaining: ' + RequestDataResponse['arenas']['current']['remainingTimer'] +
                                    '\nNext map: ' + RequestDataResponse['arenas']['next']['map'] +
                                    '```')

        #send arenas ranked maps
        await message.channel.send('**ARENAS RAKED**' +
                                    '\n```Current map: ' + RequestDataResponse['arenasRanked']['current']['map'] +
                                    '\nRemaining: ' + RequestDataResponse['arenasRanked']['current']['remainingTimer'] +
                                    ' \nNext map: ' + RequestDataResponse['arenasRanked']['next']['map'] +
                                    '```')

    if message.content.startswith('!stats '):
        RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=PC&player=' + message.content.replace('!stats ', '') + '&auth=' + APEX_TOKEN)
        RequestDataResponse = json.loads(RequestForStats.text)

        if 'Error' in RequestDataResponse:
            await message.channel.send('Error while requesting to API. Sry')
            await message.channel.send(file=discord.File('sad-cute.gif'))
            print('Error during request to API, original message: ' + message.content + ' (sent by ' + str(message.author) + '). ' + 'Error from Server: ' + RequestDataResponse)

        else:
            await message.channel.send('**' + RequestDataResponse['global']['name'] + '**`s' + ' current Legend is **' + RequestDataResponse['legends']['selected']['LegendName'] + '**')
            #await message.channel.send(RequestDataResponse['legends']['selected']['ImgAssets']['banner'])
            
            BannerImg = str(RequestDataResponse['legends']['selected']['ImgAssets']['banner'])

            filename = BannerImg.split("/")[-1]
            r = requests.get(BannerImg, stream = True)
            if r.status_code == 200:
                r.raw.decode_content = True

                with open(filename,'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            BannerImg = BannerImg.replace('https://api.mozambiquehe.re/assets/banners/', '')

            await message.channel.send(file=discord.File(BannerImg))
            await message.channel.send('**Level: ' + str(RequestDataResponse['global']['level']) + '**')
            await message.channel.send('**Status: ' + str(RequestDataResponse['realtime']['currentStateAsText']) + '**')

            if 'data' in RequestDataResponse['legends']['selected']:
                name = 'name'
                messageTracker = ['no data', 'no data', 'no data']
                CounterForFor = 0
                for name in RequestDataResponse['legends']['selected']['data']:
                    if 'name' in RequestDataResponse['legends']['selected']['data'][CounterForFor]:
                        messageTracker[CounterForFor] = RequestDataResponse['legends']['selected']['data'][CounterForFor]['name'] + ': ' + str(RequestDataResponse['legends']['selected']['data'][CounterForFor]['value'])
                        messageTracker[CounterForFor] = messageTracker[CounterForFor].replace('Special event ', '')
                        messageTracker[CounterForFor] = messageTracker[CounterForFor].capitalize()

                    CounterForFor += 1
                    
            await message.channel.send('**Trackers: **\n' +
                                        '```' + messageTracker[0] + '\n' +
                                        messageTracker[1] + '\n' +
                                        messageTracker[2] + '```')

    if message.content.startswith('!rank '):
        RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=PC&player=' + message.content.replace('!rank ', '') + '&auth=' + APEX_TOKEN)
        RequestDataResponse = json.loads(RequestForStats.text)

        if 'Error' in RequestDataResponse:
            await message.channel.send('Error while requesting to API. Sry')
            await message.channel.send(file=discord.File('sad-cute.gif'))
            print('Error during request to API, original message: ' + message.content + ' (sent by ' + message.author + '). ' + 'Error from Server: ' + RequestDataResponse)

        else:
            #await message.channel.send('**' + RequestDataResponse['global']['name'] + '**')
            #await message.channel.send('**         Rank BR: **')
            #await message.channel.send(RequestDataResponse['global']['rank']['rankImg'])
            #await message.channel.send('**          ' + str(RequestDataResponse['global']['rank']['rankScore']) + ' RP**\n' +
            #                            '\n**      Rank Arena: **')
            #await message.channel.send(RequestDataResponse['global']['arena']['rankImg'])
            #await message.channel.send('**          ' + str(RequestDataResponse['global']['arena']['rankScore']) + ' RP**')

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

            await message.channel.send(file=discord.File('output.png'))





# run the client
client.run(DISI_TOKEN)

