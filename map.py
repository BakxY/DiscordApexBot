# map go brrrr
import discord
import datetime
import requests

from log import LogFile

# class for map related functions
class Map():
    # send request to the api and store the response
    def GetData(APEX_TOKEN):
        try:
            APINotReachable = False
            # get raw data from api
            RequestForMaps = requests.get('https://api.mozambiquehe.re/maprotation?version=2&auth=' + APEX_TOKEN)
            # return received raw data and flag
            return APINotReachable, RequestForMaps

        except requests.ConnectionError as exc:
            if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
                '[Errno -2] Name or service not known' in str(exc) or # linux
                '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
                # write error to log and console
                print('[ERROR] The API is not reachable by the bot')
                LogFile.WriteLog('[ERROR] The API is not reachable by the bot')
                APINotReachable = True
                # return received raw data and flag
                return APINotReachable, RequestForMaps

    # choose right image for map
    def GetImage(map):
        if map == 'Olympus': # map is opympus
            return discord.File('src/maps/olympus.jpg')

        elif map == 'Kings Canyon': # map is kings canyon
            return discord.File('src/maps/kings-canyon.jpg')

        elif map == 'Storm Point': # map is storm point
            return discord.File('src/maps/stormpoint.jpg')

        else: #default case
            return discord.File('src/maps/mapnotavailable.jpg')

    # get status of different modes
    def GetStatus(RequestDataResponse):
        message = ''
        # add battle royale maps
        message += ('**BATTLE ROYALE**' + 
                    '\n> Current map: ' + RequestDataResponse['battle_royale']['current']['map'] +
                    '\n> Remaining: ' + RequestDataResponse['battle_royale']['current']['remainingTimer'] +
                    '\n> Next map: ' + RequestDataResponse['battle_royale']['next']['map'] +
                    '\n')

        # add battle royale ranked map
        message += ('\n**BATTLE ROYALE RANKED**' +
                    '\n> Current map: ' + RequestDataResponse['ranked']['current']['map'] +
                    '\n> Next split map: ' + RequestDataResponse['ranked']['next']['map'] +
                    '\n')

        # add arenas maps
        message += ('\n**ARENAS**' +
                    '\n> Current map: ' + RequestDataResponse['arenas']['current']['map'] +
                    '\n> Remaining: ' + RequestDataResponse['arenas']['current']['remainingTimer'] +
                    '\n> Next map: ' + RequestDataResponse['arenas']['next']['map'] +
                    '\n')

        # add arenas ranked maps
        message += ('\n**ARENAS RANKED**' +
                    '\n> Current map: ' + RequestDataResponse['arenasRanked']['current']['map'] +
                    '\n> Remaining: ' + RequestDataResponse['arenasRanked']['current']['remainingTimer'] +
                    '\n> Next map: ' + RequestDataResponse['arenasRanked']['next']['map'] +
                    '\n')

        # return message
        return message

    # configurate embed
    def ConfigEmbed(message, Image):
        # set color of embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = 'Apex Legends current maps'
        embedVar.description = message
        embedVar.set_image(url=f'attachment://{Image.filename}')
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 
        embedVar.timestamp = datetime.datetime.now()

        # return embed
        return embedVar