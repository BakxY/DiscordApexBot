# much epic disi apex bot go brrrrrrrrrrrrrrrrrrrrrrrrrr
import sys
import discord
from discord.ext import commands
from time import sleep

# import custom functions
from map import Map
from stats import Stats, StatsPlayer, StatsRank
from status import Status, Dev
from log import LogFile

# global variables
Platforms = ['PC', 'PS4', 'X1']

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

# get name of bot
mention = f'<@!{client.user.id}>'

# get the current operating system
OperatingSystem = sys.platform 

# select version of FFMPEG for os
if OperatingSystem == 'win32': # os is windows
    PathToFFMPEG = 'src/bin/ffmpeg.exe'

elif OperatingSystem == 'linux': # os is linux
    PathToFFMPEG = 'src/bin/ffmpeg-linux'

elif OperatingSystem == 'darwin': # os is macOS
    PathToFFMPEG = 'src/bin/ffmpeg-mac'

else: # os is not in list
    print('No FFMPEG version for your os')
    LogFile.WriteLog('No FFMPEG version for your os')
    exit()

#################################

# !event for start of bot

#################################

# on ready event for start of bot
@client.event
async def on_ready():
    print('Bot has connected to discord and is now online.')

#################################

# !pingall command

#################################

@client.command(brief='Pings all user in a discord', description='This command pings all user in a discord server and sends an image')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def pingall(ctx):
    await ctx.channel.send('@everyone', file=discord.File('src/ping.jpg'))

#################################

# !map command

#################################

@client.command(brief='Shows the current map rotation', description='This command displays the current map rotation of apex legends')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def map(ctx):
    # get data from api
    APINotReachable, RequestForMaps = Map.GetData(APEX_TOKEN)

    # check if API was reachable
    if APINotReachable == False: # API was reachable
        # convert request data to json format for reads
        RequestDataResponse = RequestForMaps.json()

        # get image of current map
        Image = Map.GetImage(RequestDataResponse['battle_royale']['current']['map'])

        # get stats of current modes
        message = Map.GetStatus(RequestDataResponse)

        # configurate embed message
        embedVar = Map.ConfigEmbed(message, Image)

        # send the message
        await ctx.reply(file=Image, embed=embedVar)

    else: # API was unreachable
        # write to log file and cli
        print('The API is currently not reachable by the bot')
        LogFile.WriteLog('The API is currently not reachable by the bot')

        # send error message to discord channel
        await ctx.reply('The API is currently offline', file=discord.File('src/sad-cute.gif'))

#################################

# !stats command

#################################

@client.command(brief='Shows stats of a player', description='This command displays stats of a given player')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def stats(ctx, Player):
    # create variables
    CounterForFor = 0
    PlayerFound = 0
    APINotReachable = False

    # while loop for looping over all platforms
    while PlayerFound == 0 and APINotReachable == False:
        # check if all the platforms have been checked
        if CounterForFor >= 3:
            # goto error and break
            PlayerFound = 2
            break
        
        # get player data from api
        APINotReachable, RequestForStats = Stats.GetData(Platforms[CounterForFor], Player, APEX_TOKEN)

        # check received data from api
        RequestDataResponse, PlayerFound, CounterForFor = Stats.CheckData(APINotReachable, RequestForStats, CounterForFor)
        

    if PlayerFound == 1 and APINotReachable == False: # Player exists in database
        # get trackers of player
        TrackerName, TrackerValue = StatsPlayer.GetTrackers(RequestDataResponse['legends']['selected'])

        # change X1 platform to Xbox 1 of needed
        RequestDataResponse['global']['platform'] = RequestDataResponse['global']['platform'].replace('X1', 'Xbox 1')
        
        # configurate embed message
        embedVar = StatsPlayer.ConfigEmbed(RequestDataResponse, TrackerName, TrackerValue)

        # send the message
        await ctx.reply(embed=embedVar)

    elif PlayerFound == 2: # player not found or error
        # send error message to discord channel
        await ctx.reply(RequestDataResponse['Error'], file=discord.File('src/sad-cute.gif'))

        # print error message to cli and log file
        print('Error during request to API, message from API: ' + str(RequestDataResponse))
        LogFile.WriteLog('Error during request to API, message from API: ' + str(RequestDataResponse))
    
    elif APINotReachable == True:
        # write to log file and cli
        print('The API is currently not reachable by the bot')
        LogFile.WriteLog('The API is currently not reachable by the bot')

        # send error message to discord channel
        await ctx.reply('The API is currently offline', file=discord.File('src/sad-cute.gif'))

#################################

# !rank command

#################################

@client.command(brief='Shows ranks of a player', description='This command displays ranks of a given player')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def rank(ctx, Player):
    PlayerFound = 0
    CounterForFor= 0

    # while loop for looping over all platforms
    while PlayerFound == 0 and APINotReachable == False:
        # check if all the platforms have been checked
        if CounterForFor >= 3:
            # goto error and break
            PlayerFound = 2
            break

        # get player data from api
        APINotReachable, RequestForStats = Stats.GetData(Platforms[CounterForFor], Player, APEX_TOKEN)

        # check received data from api
        RequestDataResponse, PlayerFound, CounterForFor = Stats.CheckData(APINotReachable, RequestForStats, CounterForFor)

    if PlayerFound == 1 and APINotReachable == False: # Player exists in database
        
        # configure naming of ranks
        RequestDataResponse = StatsRank.ConfigRanks(RequestDataResponse)

        # configure embed for battle royale ranked
        embedVar = StatsRank.ConfigEmbedBR(RequestDataResponse)

        # send the message
        await ctx.reply(embed=embedVar)

        # configure embed for arena ranked
        embedVar = StatsRank.ConfigEmbedAR(RequestDataResponse)

        # send the message
        await ctx.reply(embed=embedVar)

    elif PlayerFound == 2: # player not found or error
        # send error message to discord channel
        await ctx.reply(RequestDataResponse['Error'], file=discord.File('src/sad-cute.gif'))

        # print error message to cli and log file
        print('Error during request to API, message from API: ' + str(RequestDataResponse))
        LogFile.WriteLog('Error during request to API, message from API: ' + str(RequestDataResponse))

    elif APINotReachable == True:
        # write to log file and cli
        print('The API is currently not reachable by the bot')
        LogFile.WriteLog('The API is currently not reachable by the bot')

        # send error message to discord channel
        await ctx.reply('The API is currently offline', file=discord.File('src/sad-cute.gif'))
        
#################################

# !status command

#################################

@client.command(brief='Shows the status of all servers', description='This command lists all the servers with theire status')
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def status(ctx):
    # get server data from api
    APINotReachable, RequestForStatus = Status.GetData(APEX_TOKEN)

    # check if the API was reachable
    if APINotReachable == False:
        # convert request data to json format for reads
        RequestDataResponse = RequestForStatus.json()

        # create message of all server states
        message = Status.GetStatus(RequestDataResponse)

        # configurate embed
        embedVar = Status.ConfigEmbed(message)
        
        # define the image
        Image = discord.File('src/ApexServer.png')
        
        # send the message
        await ctx.reply(file=Image, embed=embedVar)
    
    else:
        # write to log file and cli
        print('The API is currently not reachable by the bot')
        LogFile.WriteLog('The API is currently not reachable by the bot')

        # send error message to discord channel
        await ctx.reply('The API is currently offline', file=discord.File('src/sad-cute.gif'))

#################################

# !dev command

#################################

@client.command(brief='Shows infos about bot and devs', description='This command shows come infos about the bot and its creators', aliases=['about', 'devs', 'info'])
@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
async def dev(ctx):
    # send embed with credits
    await ctx.reply(embed=Dev.Creators())

#################################

#! @bot ping

#################################

@client.event
async def on_message(message):
    # check if bot has been mentioned as an @ ping
    if mention in message.content:
        # get the context for the ping message
        ctx = await client.get_context(message)
        # check if author of message is in voice channeö
        if not ctx.message.author.voice:
            # send message to text channel
            await ctx.reply('{} is not connected to a voice channel'.format(ctx.message.author.name))
            return
        else:
            # set the channel to author channel
            channel = ctx.message.author.voice.channel

        # connect to voice channel
        vc = await channel.connect()

        # play sound file using FFMPEG
        vc.play(discord.FFmpegPCMAudio(executable=PathToFFMPEG, source='src/sound/dafuq.mp3'))

        # wait for 5 seconds so the file can finish playing
        sleep(5)

        # leave the voice channel
        await vc.disconnect()

    # give the message to the command handler
    await client.process_commands(message)

# run the discord bot with the discord token
client.run(DISI_TOKEN)
