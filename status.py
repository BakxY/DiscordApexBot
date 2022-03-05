# server status go brrr
import discord
import datetime
import requests

from log import LogFile

# class for server status related functions
class Status():
    # send request to the api and store the response
    def GetData(APEX_TOKEN):
        try:
            APINotReachable = False
            # get raw data from api
            RequestForStatus = requests.get('https://api.mozambiquehe.re/servers?auth=' + APEX_TOKEN)
            # return received raw data and flag
            return APINotReachable, RequestForStatus

        except requests.ConnectionError as exc:
            if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
                '[Errno -2] Name or service not known' in str(exc) or # linux
                '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
                # write error to log and console
                print('[ERROR] The API is not reachable by the bot')
                LogFile.WriteLog('[ERROR] The API is not reachable by the bot')
                APINotReachable = True
                # return received raw data and flag
                return APINotReachable, RequestForStatus
            else:
                raise exc

    # build message with all server states
    def GetStatus(RequestDataResponse):
        CounterForFor, ServerType, ServerLoc, message = 0, 0, 0, ''

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
        
        # return message with all server states
        return message

    # configurate embed
    def ConfigEmbed(message):
        # define a new embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = 'EA Server current status'
        embedVar.description = message
        embedVar.set_image(url='attachment://ApexServer.png')
        embedVar.set_footer(text='More data on apexlegendsstatus.com')
        embedVar.timestamp = datetime.datetime.now()

        # return embed
        return embedVar

# class for developer related functions
class Dev():
    # functions for credits
    def Creators():
        message = ''
    
        # define a new embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # add text to message
        message += ('**About the bot**\n' +
        'This is a discord bot with integration for Apex Legends. It can show the current map, stats, status of servers and ranks of players. The bot was created out of boredom during the COVID-19 pandemic.\n')

        # add space
        message += '_ _\n'

        # add text to message
        message += ('**Devs**\n' +
        'This bot was programmed by BakxY and FischerTG. The current code is written in Python, but we will switch to JavaScript soon. All the code can be found on Github.\n')

        # add space
        message += '_ _\n'

        # add link to Github
        message += 'Source code: https://github.com/BakxY/DiscordApexBot'

        # set all parameters for the embed
        embedVar.description = message
        embedVar.timestamp = datetime.datetime.now()

        # return embed
        return embedVar