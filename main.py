# much epic disi apex bot go brrrrrrrrrrrrrrrrrrrrrrrrrr
import sys
from typing import Counter
import discord
from discord.ext import commands
import json
import requests
import time

from log import *

# get discord api key form file
DISI_TOKEN_FILE = open('src/token/DISI_API_TOKEN', 'r')
DISI_TOKEN = DISI_TOKEN_FILE.read()
DISI_TOKEN = DISI_TOKEN.replace('\n', '')
DISI_TOKEN_FILE.close()

# get apex api key form file
APEX_TOKEN_FILE = open('src/token/APEX_API_TOKEN', 'r')
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
        APINotReachable = False
        # send request to the api and store the response
        RequestForMaps = requests.get('https://api.mozambiquehe.re/maprotation?version=2&auth=' + APEX_TOKEN)

    except requests.ConnectionError as exc:
        if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
            '[Errno -2] Name or service not known' in str(exc) or # linux
            '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
            print('[ERROR] The API is not reachable by the bot')
            APINotReachable = True

    if APINotReachable == False:
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
        embedVar.title = 'Apex Legends current maps'
        embedVar.description = message
        embedVar.set_image(url=f'attachment://{Image.filename}')
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 

        # send the message
        await ctx.reply(file=Image, embed=embedVar)
    else:
        # send error message to discord channel
        await ctx.reply('The API is currently offline')
        await ctx.reply(file=discord.File('src/sad-cute.gif'))








@client.command(brief='Shows stats of a player', description='This command displays stats of a given player')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def stats(ctx, Player):
    # create variables
    PlayerFound, CounterForFor, Platforms, message = 0, 0, ['PC', 'PS4', 'X1'], ''
    APINotReachable = False

    while PlayerFound == 0 and APINotReachable == False:
        # check if all the platforms have been checked
        if CounterForFor >= 3:
            # goto error and break
            PlayerFound = 2
            break

        # send request to the api and store the response
        try:
            RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=' + Platforms[CounterForFor] + '&player=' + Player + '&auth=' + APEX_TOKEN)

        except requests.ConnectionError as exc:
            if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
                '[Errno -2] Name or service not known' in str(exc) or # linux
                '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
                print('[ERROR] The API is not reachable by the bot')
                APINotReachable = True

            else:
                raise exc
        
        if APINotReachable == False:
            RequestDataResponse = json.loads(RequestForStats.text)

            # check if the api sent a error
            if 'Error' in RequestDataResponse: 
                PlayerFound = 0
            elif 'global' in RequestDataResponse:
                PlayerFound = 1

            CounterForFor += 1
        

    if PlayerFound == 1 and APINotReachable == False: # Player exists in database
        if 'data' in RequestDataResponse['legends']['selected']:
            name = 'name'
            # set the messages for trackers to default
            TrackerName = ['no data', 'no data', 'no data']
            TrackerValue = ['no data', 'no data', 'no data']

            CounterForFor = 0
            
            # loop for every tracker equiped
            for name in RequestDataResponse['legends']['selected']['data']: 
                if 'name' in RequestDataResponse['legends']['selected']['data'][CounterForFor]:
                    TrackerName[CounterForFor] = RequestDataResponse['legends']['selected']['data'][CounterForFor]['name']
                    TrackerName[CounterForFor] = TrackerName[CounterForFor].replace('Special event ', '')
                    TrackerName[CounterForFor] = TrackerName[CounterForFor].capitalize()

                    TrackerValue[CounterForFor] = str(RequestDataResponse['legends']['selected']['data'][CounterForFor]['value'])

                CounterForFor += 1

        # change X1 platform to Xbox 1 of needed
        RequestDataResponse['global']['platform'] = RequestDataResponse['global']['platform'].replace('X1', 'Xbox 1')
        
        # set color of embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = RequestDataResponse['global']['name'] + ' as ' + RequestDataResponse['legends']['selected']['LegendName']
        
        # display some standart stats
        embedVar.add_field(name='Level', value=str(RequestDataResponse['global']['level']), inline=True)
        embedVar.add_field(name='BP-Level', value=str(RequestDataResponse['global']['battlepass']['level']), inline=True)
        embedVar.add_field(name='_ _', value='_ _', inline=False)
        embedVar.add_field(name='Status', value=RequestDataResponse['realtime']['currentStateAsText'], inline=True)
        embedVar.add_field(name='Platform', value=RequestDataResponse['global']['platform'], inline=True)

        # spaces
        embedVar.add_field(name='_ _', value='_ _', inline=False)
        embedVar.add_field(name='Trackers:', value='_ _', inline=False)

        # display current trackers
        embedVar.add_field(name=TrackerName[0], value=TrackerValue[0], inline=True)
        embedVar.add_field(name=TrackerName[1], value=TrackerValue[1], inline=True)
        embedVar.add_field(name=TrackerName[2], value=TrackerValue[2], inline=True)
        
        # set image and thumbnail
        embedVar.set_image(url=str(RequestDataResponse['legends']['selected']['ImgAssets']['banner']))
        embedVar.set_thumbnail(url=str(RequestDataResponse['legends']['selected']['ImgAssets']['icon']))

        # set footer and timestamp
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 
        embedVar.timestamp = datetime.datetime.now()

        # send the message
        await ctx.reply(embed=embedVar)

    elif PlayerFound == 2: # player not found or error
        # send error message to discord channel
        await ctx.reply(RequestDataResponse['Error'])
        await ctx.reply(file=discord.File('src/sad-cute.gif'))
        # print error message to cli
        print('Error during request to API, message from API: ' + str(RequestDataResponse))
    
    elif APINotReachable == True:
        # send error message to discord channel
        await ctx.reply('The API is currently offline')
        await ctx.reply(file=discord.File('src/sad-cute.gif'))







@client.command(brief='Shows ranks of a player', description='This command displays ranks of a given player')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def rank(ctx, Player):
    PlayerFound, CounterForFor, Platforms = 0, 0, ['PC', 'PS4', 'X1']
    APINotReachable = False

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
            if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
                '[Errno -2] Name or service not known' in str(exc) or # linux
                '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
                print('[ERROR] The API is not reachable by the bot')
                APINotReachable = True
            else:
                raise exc
                
        if APINotReachable == False:    
            RequestDataResponse = json.loads(RequestForStats.text)

            # check if the api sent a error
            if 'Error' in RequestDataResponse: 
                PlayerFound = 0
            elif 'global' in RequestDataResponse:
                PlayerFound = 1

            CounterForFor += 1

    if PlayerFound == 1 and APINotReachable == False: # Player exists in database
        message = ''

        RequestDataResponse['global']['rank']['rankedSeason']  = RequestDataResponse['global']['rank']['rankedSeason'].replace('season', 'Season ')
        RequestDataResponse['global']['rank']['rankedSeason']  = RequestDataResponse['global']['rank']['rankedSeason'].replace('_split_', '')
        RequestDataResponse['global']['rank']['rankedSeason']  = RequestDataResponse['global']['rank']['rankedSeason'][:-1]

        RequestDataResponse['global']['arena']['rankedSeason']  = RequestDataResponse['global']['arena']['rankedSeason'].replace('arenas', 'Season ')
        RequestDataResponse['global']['arena']['rankedSeason']  = RequestDataResponse['global']['arena']['rankedSeason'].replace('_split_', '')
        RequestDataResponse['global']['arena']['rankedSeason']  = RequestDataResponse['global']['arena']['rankedSeason'][:-1]
        
        # set color of embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = RequestDataResponse['global']['name'] + ' in BR ranked ' + RequestDataResponse['global']['rank']['rankedSeason']

        # create fields for infos
        embedVar.add_field(name='Current Rank', value=RequestDataResponse['global']['rank']['rankName'] + ' ' + str(RequestDataResponse['global']['rank']['rankDiv']), inline=True)
        embedVar.add_field(name='Current RP', value=str(RequestDataResponse['global']['rank']['rankScore']) + ' RP', inline=True)

        # set thumbnail
        embedVar.set_thumbnail(url=str(RequestDataResponse['global']['rank']['rankImg']))

        # set footer and timestamp
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 
        embedVar.timestamp = datetime.datetime.now()

        # send the message
        await ctx.reply(embed=embedVar)

        # remove the old fields
        embedVar.remove_field(-1)
        embedVar.remove_field(-1)
        
        # set all parameters for the embed
        embedVar.title = RequestDataResponse['global']['name'] + ' in arenas ranked ' + RequestDataResponse['global']['arena']['rankedSeason']

        # create fields for infos
        embedVar.add_field(name='Current Rank', value=RequestDataResponse['global']['arena']['rankName'] + ' ' + str(RequestDataResponse['global']['arena']['rankDiv']), inline=True)
        embedVar.add_field(name='Current RP', value=str(RequestDataResponse['global']['arena']['rankScore']) + ' RP', inline=True)

        # set thumbnail
        embedVar.set_thumbnail(url=str(RequestDataResponse['global']['arena']['rankImg']))

        # send the message
        await ctx.reply(embed=embedVar)

    elif PlayerFound == 2: # player not found or error
        # send error message to discord channel
        await ctx.reply(RequestDataResponse['Error'])
        await ctx.reply(file=discord.File('src/sad-cute.gif'))
        # print error message to cli
        print('Error during request to API, message from API: ' + str(RequestDataResponse))

    elif APINotReachable == True:
        # send error message to discord channel
        await ctx.reply('The API is currently offline')
        await ctx.reply(file=discord.File('src/sad-cute.gif'))








@client.command(brief='Shows the status of all servers', description='This command lists all the servers with theire status')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def status(ctx):
    APINotReachable, CounterForFor, message, ServerType, ServerLoc = False, 0, '', 0, 0

    try:
            RequestForStats = requests.get('https://api.mozambiquehe.re/servers?auth=' + APEX_TOKEN)
    except requests.ConnectionError as exc:
        if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
            '[Errno -2] Name or service not known' in str(exc) or # linux
            '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
            print('[ERROR] The API is not reachable by the bot')
            APINotReachable = True
        else:
            raise exc

    if APINotReachable == False:
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
        embedVar.title = 'EA Server current status'
        embedVar.description = message
        embedVar.set_image(url='attachment://ApexServer.png')
        embedVar.set_footer(text='More data on apexlegendsstatus.com')
        embedVar.timestamp = datetime.datetime.now()
        
        # define the image
        Image = discord.File('src/ApexServer.png')
        
        # send the message
        await ctx.reply(file=Image, embed=embedVar)

@client.command(brief='Shows infos about bot and devs', description='This command shows come infos about the bot and its creators', aliases=['about', 'devs', 'info'])
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def dev(ctx):
    message = ''
    
    embedVar = discord.Embed(color=0xEF2AEF)

    message += ('**About the bot**\n' +
    'This is an discord bot with inegration for apex legends. It can show the current map, stats, status of servers and ranks of players. The bot was created out of boredom during the COVID-19 pandamic.\n')

    message += '_ _\n'

    message += ('**Devs**\n' +
    'The bot was programmed by BakxY and FischerTG. The current code is written in Python, but the we will switch to JavaScript shortly. All the code can be found on github.\n')

    message += '_ _\n'

    message += 'Source code: https://github.com/BakxY/DiscordApexBot'

    embedVar.description = message

    embedVar.timestamp = datetime.datetime.now()

    await ctx.reply(embed=embedVar)

@client.event
async def on_message(message):
    mention = f'<@!{client.user.id}>'
    if mention in message.content:
        ctx = await client.get_context(message)
        if not ctx.message.author.voice:
            await ctx.reply('{} is not connected to a voice channel'.format(ctx.message.author.name))
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

