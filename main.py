# much epic disi apex bot go brrrrrrrrrrrrrrrrrrrrrrrrrr
from pickle import FALSE, TRUE
import sys
from typing import Counter
import discord
from discord.ext import commands
import json
import requests
import time

from rank import *
from log import *

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
        message = ''
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
            Image = discord.File('src/maps/olympus.jpg')

        elif RequestDataResponse['battle_royale']['current']['map'] == 'Kings Canyon': # map is kings canyon
            Image = discord.File('src/maps/kings-canyon.jpg')

        elif RequestDataResponse['battle_royale']['current']['map'] == 'Storm Point': # map is storm point
            Image = discord.File('src/maps/stormpoint.jpg')

        else: #default case
            message += ('```diff' +
                        'Map image not implemented yet.'
                        '```\n')


        # send battle royale maps
        message += ('**BATTLE ROYALE**' + 
                    '\n> Current map: ' + RequestDataResponse['battle_royale']['current']['map'] +
                    '\n> Remaining: ' + RequestDataResponse['battle_royale']['current']['remainingTimer'] +
                    '\n> Next map: ' + RequestDataResponse['battle_royale']['next']['map'] +
                    '\n')

        #send battle royale ranked map
        message += ('\n**BATTLE ROYALE RANKED**' +
                    '\n> Current map: ' + RequestDataResponse['ranked']['current']['map'] +
                    '\n> Next split map: ' + RequestDataResponse['ranked']['next']['map'] +
                    '\n')

        #send arenas maps
        message += ('\n**ARENAS**' +
                    '\n> Current map: ' + RequestDataResponse['arenas']['current']['map'] +
                    '\n> Remaining: ' + RequestDataResponse['arenas']['current']['remainingTimer'] +
                    '\n> Next map: ' + RequestDataResponse['arenas']['next']['map'] +
                    '\n')

        #send arenas ranked maps
        message += ('\n**ARENAS RANKED**' +
                    '\n> Current map: ' + RequestDataResponse['arenasRanked']['current']['map'] +
                    '\n> Remaining: ' + RequestDataResponse['arenasRanked']['current']['remainingTimer'] +
                    '\n> Next map: ' + RequestDataResponse['arenasRanked']['next']['map'] +
                    '\n')

        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = "Apex Legends current maps"
        embedVar.description = message
        embedVar.set_image(url=f'attachment://{Image.filename}')
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 

        # send the message
        await ctx.send(file=Image, embed=embedVar)
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
                                '**Status: ' + str(RequestDataResponse['realtime']['currentStateAsText']) + '**')

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
        # download badges
        RankImage_DownloadBadges(RequestDataResponse['global']['rank'], RequestDataResponse['global']['arena'])

        # create image
        RankImage_Create()

        # write player name
        RankImage_PlayerName(RequestDataResponse['global']['name'])

        # add BR badge parts
        RankImage_BRbadge(RequestDataResponse['global']['rank'])

        # add AR badge parts
        RankImage_ARbadge(RequestDataResponse['global']['arena'])

        # save image
        RankImage_Save()

        # send picture to channel
        await ctx.channel.send(file=discord.File('src/rank/rank.png'))

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








@client.command(brief='Shows the status of all servers', description='This command lists all the servers with theire status')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def status(ctx):
    APINotReachable, CounterForFor, message, ServerType, ServerLoc = FALSE, 0, '', 0, 0

    try:
            RequestForStats = requests.get('https://api.mozambiquehe.re/servers?auth=' + APEX_TOKEN)
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

        for i in RequestDataResponse: # repeat for every index in RequestDataResponse
            if CounterForFor >= 3: # check if all needed data has been outputted
                break
            
            # go from placeholder to variable
            ServerType = i

            message += '\n **' + ServerType.replace('_', ' ') + '**\n' # add server type to the message

            for j in RequestDataResponse[i]: # repeat for every index in RequestDataResponse[i]

                # go from placeholder to variable
                ServerLoc = j

                # case for every status
                if RequestDataResponse[i][j]['Status'] == 'UP':
                    message += ':green_circle: '

                elif RequestDataResponse[i][j]['Status'] == 'DOWN':
                    message += ':red_circle: '

                elif RequestDataResponse[i][j]['Status'] == 'SLOW':
                    message += ':orange_circle: '

                elif RequestDataResponse[i][j]['Status'] == 'OVERLOADED':
                    message += ':yellow_circle: '

                elif RequestDataResponse[i][j]['Status'] == 'NO DATA':
                    message += ':zzz:  '

                message += ServerLoc + '\n'

            CounterForFor += 1

        # define a new embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = "EA Server current status"
        embedVar.description = message
        embedVar.set_image(url='attachment://ApexServer.png')
        embedVar.set_footer(text='More data on apexlegendsstatus.com')
        
        # define the image
        Image = discord.File("src/ApexServer.png")
        
        # send the message
        await ctx.send(file=Image, embed=embedVar)


@client.event
async def on_message(message):
    mention = f'<@!{client.user.id}>'
    if mention in message.content:
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

