# much epic disi apex bot go brrrrrrrrrrrrrrrrrrrrrrrrrr
import os
from pickle import FALSE, TRUE
import sys
from typing import Counter
import discord
from discord.ext import commands
import json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
import shutil
import urllib.request
import time

#import and create fonts
DisiFont15 = ImageFont.truetype("src/fonts/font.ttf", 15)
DisiFont20 = ImageFont.truetype("src/fonts/font.ttf", 20)

# get discord api key form file
DISI_TOKEN_FILE = open("src/token/DISI_API_TOKEN", 'r')
DISI_TOKEN = DISI_TOKEN_FILE.read()
DISI_TOKEN = DISI_TOKEN.replace('\n', '')
DISI_TOKEN_FILE.close()

# get apex api key form file
APEX_TOKEN_FILE = open("src/token/APEX_API_TOKEN", 'r')
APEX_TOKEN = APEX_TOKEN_FILE.read()
APEX_TOKEN = APEX_TOKEN.replace('\n', '')
APEX_TOKEN_FILE.close()

# create bot with a command prefix
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
client = commands.Bot(
    command_prefix = commands.when_mentioned_or('!'),
    description = 'This a bot for discord, that can display stats, rankings and current maps for apex legends.',
    help_command = help_command
)

OperatingSystem = sys.platform # get the current operating system

if OperatingSystem == 'win32': # os is windows
    PathToFFMPEG = 'src/bin/ffmpeg.exe'

elif OperatingSystem == 'linux': # os is linux
    PathToFFMPEG = 'src/bin/ffmpeg-linux'

elif OperatingSystem == 'darwin': # os is macOS
    PathToFFMPEG = 'src/bin/ffmpeg-mac'

else: # os is not in list
    print('No FFMPEG version for you os')
    exit()

# create width and height for ranked image
W, H = 250, 250

# on ready event for start of bot
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')








@client.command(brief='Pings all user in a discord', description='This command pings all user in a discord server and sends an image')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def pingall(ctx):
    await ctx.channel.send('@everyone')
    await ctx.channel.send(file=discord.File('src/ping.jpg'))








@client.command(brief='Shows the current map rotation', description='This command displays the current map rotation of apex legends')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def map(ctx):
    try:
        APINotReachable = FALSE
        # send request to the api and store the response
        RequestForMaps = requests.get('https://api.mozambiquehe.re/maprotation?version=2&auth=' + APEX_TOKEN)

    except requests.ConnectionError as exc:
        if("[Errno 11001] getaddrinfo failed" in str(exc) or # windows
            "[Errno -2] Name or service not known" in str(exc) or # linux
            "[Errno 8] nodename nor servname " in str(exc)): # Mac OS
            print('[ERROR] The API is not reachable by the bot')
            APINotReachable = TRUE

    if APINotReachable == FALSE:
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
    else:
        # send error message to discord channel
        await ctx.channel.send('The API is currently offline')
        await ctx.channel.send(file=discord.File('src/sad-cute.gif'))








@client.command(brief='Shows stats of a player', description='This command displays stats of a given player')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def stats(ctx, Player):
    # create variables
    PlayerFound, CounterForFor, Platforms = 0, 0, ['PC', 'PS4', 'X1']
    APINotReachable = FALSE

    while PlayerFound == 0 and APINotReachable == FALSE:
        # check if all the platforms have been checked
        if CounterForFor >= 3:
            # goto error and break
            PlayerFound = 2
            break

        # send request to the api and store the response
        try:
            RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=' + Platforms[CounterForFor] + '&player=' + Player + '&auth=' + APEX_TOKEN)

        except requests.ConnectionError as exc:
            if("[Errno 11001] getaddrinfo failed" in str(exc) or # windows
                "[Errno -2] Name or service not known" in str(exc) or # linux
                "[Errno 8] nodename nor servname " in str(exc)): # Mac OS
                print('[ERROR] The API is not reachable by the bot')
                APINotReachable = TRUE

            else:
                raise exc
        
        if APINotReachable == FALSE:
            RequestDataResponse = json.loads(RequestForStats.text)

            # check if the api sent a error
            if 'Error' in RequestDataResponse: 
                PlayerFound = 0
            elif 'global' in RequestDataResponse:
                PlayerFound = 1

            CounterForFor += 1
        

    if PlayerFound == 1 and APINotReachable == FALSE: # Player exists in database
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
    
    elif APINotReachable == TRUE:
        # send error message to discord channel
        await ctx.channel.send('The API is currently offline')
        await ctx.channel.send(file=discord.File('src/sad-cute.gif'))







@client.command(brief='Shows ranks of a player', description='This command displays ranks of a given player')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def rank(ctx, Player):
    PlayerFound, CounterForFor, Platforms = 0, 0, ['PC', 'PS4', 'X1']
    APINotReachable = FALSE

    while PlayerFound == 0:
        # check if all the platforms have been checked
        if CounterForFor >= 3:
            # goto error and break
            PlayerFound = 2
            break

        # send request to the api and store the response
        try:
            RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=' + Platforms[CounterForFor] + '&player=' + Player + '&auth=' + APEX_TOKEN)
        except requests.ConnectionError as exc:
            if("[Errno 11001] getaddrinfo failed" in str(exc) or # windows
                "[Errno -2] Name or service not known" in str(exc) or # linux
                "[Errno 8] nodename nor servname " in str(exc)): # Mac OS
                print('[ERROR] The API is not reachable by the bot')
                APINotReachable = TRUE
            else:
                raise exc
                
        if APINotReachable == FALSE:    
            RequestDataResponse = json.loads(RequestForStats.text)

            # check if the api sent a error
            if 'Error' in RequestDataResponse: 
                PlayerFound = 0
            elif 'global' in RequestDataResponse:
                PlayerFound = 1

            CounterForFor += 1

    if PlayerFound == 1 and APINotReachable == FALSE: # Player exists in database
        # download BR rank image and store it
        RankImgRequest = requests.get(RequestDataResponse['global']['rank']['rankImg'], allow_redirects=True, stream=True)
        with open('src/rank/' + RequestDataResponse['global']['rank']['rankName'] + str(RequestDataResponse['global']['rank']['rankDiv']) + '.png','wb') as f:
            shutil.copyfileobj(RankImgRequest.raw, f)

        # download AR rank image and store it
        RankImgRequest = requests.get(RequestDataResponse['global']['arena']['rankImg'], allow_redirects=True, stream=True)
        with open('src/rank/' + RequestDataResponse['global']['arena']['rankName'] + str(RequestDataResponse['global']['arena']['rankDiv']) + '.png','wb') as f:
            shutil.copyfileobj(RankImgRequest.raw, f)

        # create new image to edit
        img = Image.new('RGBA', (W, H))
        img1draw = ImageDraw.Draw(img)

        # write player name text
        FontSize = 25
        w = W + 1
        while w > W:
            NameFont = ImageFont.truetype("src/fonts/font.ttf", FontSize)
            w, h = img1draw.textsize(RequestDataResponse['global']['name'], font=NameFont)
            if FontSize == 1:
                break
            FontSize -= 1
        img1draw.text(((W - w) / 2, 0), RequestDataResponse['global']['name'], fill="white", font=NameFont)

        # write BR Rank text
        w1, h1 = img1draw.textsize('BR Rank', font=DisiFont20)
        img1draw.text((((W / 2) - w1) / 2, h + 10), 'BR Rank', fill='white', font=DisiFont20)

        # write AR Rank text
        w1, h1 = img1draw.textsize('AR Rank', font=DisiFont20)
        img1draw.text(((((W / 2) - w1) / 2) + (W / 2), h + 10), 'AR Rank', fill='white', font=DisiFont20)
        
        # draw BR Rank symbol
        imgrank = Image.open('src/rank/' + RequestDataResponse['global']['rank']['rankName'] + str(RequestDataResponse['global']['rank']['rankDiv']) + '.png')
        imgrank = imgrank.resize((120, 120), Image.ADAPTIVE)
        area = (int(((W / 2) - 120) / 2), h + h1 + 20, int(((W / 2) - 120) / 2) + 120, h + h1 + 140)
        img.paste(imgrank, area)
        imgrank.close()

        # check if predator badge was placed
        if 'Apex Predator' == RequestDataResponse['global']['rank']['rankName']:
            # write Predator rank
            w2, h2 = img1draw.textsize('#' + str(RequestDataResponse['global']['rank']['ladderPosPlatform']), font=DisiFont15)
            img1draw.text(((((W / 2) - w2) / 2), h + h1 + 113), '#' + str(RequestDataResponse['global']['rank']['ladderPosPlatform']), fill='white', font=DisiFont15)

        # draw AR Rank symbol
        imgrank = Image.open('src/rank/' + RequestDataResponse['global']['arena']['rankName'] + str(RequestDataResponse['global']['arena']['rankDiv']) + '.png')
        imgrank = imgrank.resize((120, 120), Image.ADAPTIVE)
        area = (int(((W / 2) - 120) / 2 + (W / 2)), h + h1 + 20, int(((W / 2) - 120) / 2 + (W / 2)) + 120, h + h1 + 140)
        img.paste(imgrank, area)
        imgrank.close()

        # check if predator badge was placed
        if 'Apex Predator' == RequestDataResponse['global']['arena']['rankName']:
            # write Predator rank
            w2, h2 = img1draw.textsize('#' + str(RequestDataResponse['global']['arena']['ladderPosPlatform']), font=DisiFont15)
            img1draw.text(((((W / 2) - w2) / 2) + (W / 2), h + h1 + 113), '#' + str(RequestDataResponse['global']['arena']['ladderPosPlatform']), fill='white', font=DisiFont15)

        # write BR Rank value
        w1, h1 = img1draw.textsize(str(RequestDataResponse['global']['rank']['rankScore']) + 'RP', font=DisiFont20)
        img1draw.text((((W / 2) - w1) / 2, h + h1 + 150), str(RequestDataResponse['global']['rank']['rankScore']) + 'RP', fill='white', font=DisiFont20)

        # write AR Rank value
        w1, h1 = img1draw.textsize(str(RequestDataResponse['global']['arena']['rankScore']) + 'AP', font=DisiFont20)
        img1draw.text(((((W / 2) - w1) / 2) + (W / 2), h + h1 + 150), str(RequestDataResponse['global']['arena']['rankScore']) + 'AP', fill='white', font=DisiFont20)

        # save picture
        img.save('output.png')
        img.close()

        # send picture to channel
        await ctx.channel.send(file=discord.File('output.png'))

    elif PlayerFound == 2: # player not found or error
        # send error message to discord channel
        await ctx.channel.send(RequestDataResponse['Error'])
        await ctx.channel.send(file=discord.File('src/sad-cute.gif'))
        # print error message to cli
        print('Error during request to API, message from API: ' + str(RequestDataResponse))

    elif APINotReachable == TRUE:
        # send error message to discord channel
        await ctx.channel.send('The API is currently offline')
        await ctx.channel.send(file=discord.File('src/sad-cute.gif'))








@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        ctx = await client.get_context(message)
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel

        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable=PathToFFMPEG, source='src/sound/dafuq.mp3'))

        time.sleep(2)

        await vc.disconnect()
    await client.process_commands(message)

# run the client
client.run(DISI_TOKEN)

