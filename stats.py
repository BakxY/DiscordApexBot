# player stats go brrr
import discord
import datetime
import requests

from log import LogFile

# class for functions used for player stats and ranked stats
class Stats():
    # send request to the api and store the response
    def GetData(Platform, Player, APEX_TOKEN):
        try:
            APINotReachable = False
            # get raw data from api
            RequestForStats = requests.get('https://api.mozambiquehe.re/bridge?version=5&platform=' + Platform + '&player=' + Player + '&auth=' + APEX_TOKEN)
            # return received raw data and flag
            return APINotReachable, RequestForStats

        except requests.ConnectionError as exc:
            if('[Errno 11001] getaddrinfo failed' in str(exc) or # windows
                '[Errno -2] Name or service not known' in str(exc) or # linux
                '[Errno 8] nodename nor servname ' in str(exc)): # Mac OS
                # write error to log and console
                print('[ERROR] The API is not reachable by the bot')
                LogFile.WriteLog('[ERROR] The API is not reachable by the bot')
                APINotReachable = True
                # return received raw data and flag
                return APINotReachable, RequestForStats

            else:
                raise exc

    # check the data received from the api
    def CheckData(APINotReachable, RequestForStats, CounterForFor):
        if APINotReachable == False:
            # convert to json
            RequestDataResponse = RequestForStats.json()

            # check if the api sent a error
            if 'Error' in RequestDataResponse: 
                PlayerFound = 0
            elif 'global' in RequestDataResponse:
                PlayerFound = 1

            CounterForFor += 1
            # return received data and flags
            return RequestDataResponse, PlayerFound, CounterForFor

# class for functions only related to player stats
class StatsPlayer():
    # get trackers of player
    def GetTrackers(selected_legend):
        # set the messages for trackers to default
        TrackerName = ['no data', 'no data', 'no data']
        TrackerValue = ['no data', 'no data', 'no data']
        if 'data' in selected_legend:
            name = 'name'
            CounterForFor = 0
            
            # loop for every tracker equiped
            for name in selected_legend['data']: 
                if 'name' in selected_legend['data'][CounterForFor]:
                    # store traker name
                    TrackerName[CounterForFor] = selected_legend['data'][CounterForFor]['name']
                    # remove special event text from special event badges and capitalize
                    TrackerName[CounterForFor] = TrackerName[CounterForFor].replace('Special event ', '')
                    TrackerName[CounterForFor] = TrackerName[CounterForFor].capitalize()
                    # store value of traker
                    TrackerValue[CounterForFor] = str(selected_legend['data'][CounterForFor]['value'])

                CounterForFor += 1
        
        # return tracker arrays
        return TrackerName, TrackerValue

    # configure embed for player stats
    def ConfigEmbed(RequestDataResponse, TrackerName, TrackerValue):
        # set color of embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = RequestDataResponse['global']['name'] + ' as ' + RequestDataResponse['legends']['selected']['LegendName']
        
        # display some standard stats
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

        # return embed message
        return embedVar

# class for functions only related to ranked stats 
class StatsRank():
    # removing unnecessary text and capitalize where necessary
    def ConfigRanks(RequestDataResponse):
        # edit battle royale rank text
        RequestDataResponse['global']['rank']['rankedSeason']  = RequestDataResponse['global']['rank']['rankedSeason'].replace('season', 'Season ')
        RequestDataResponse['global']['rank']['rankedSeason']  = RequestDataResponse['global']['rank']['rankedSeason'].replace('_split_', '')
        RequestDataResponse['global']['rank']['rankedSeason']  = RequestDataResponse['global']['rank']['rankedSeason'][:-1]
        
        # edit arena rank text
        RequestDataResponse['global']['arena']['rankedSeason']  = RequestDataResponse['global']['arena']['rankedSeason'].replace('arenas', 'Season ')
        RequestDataResponse['global']['arena']['rankedSeason']  = RequestDataResponse['global']['arena']['rankedSeason'].replace('_split_', '')
        RequestDataResponse['global']['arena']['rankedSeason']  = RequestDataResponse['global']['arena']['rankedSeason'][:-1]
        
        # return edited data
        return RequestDataResponse

    # configure embed for battle royale rank
    def ConfigEmbedBR(RequestDataResponse):
        # set color of embed
        embedVar = discord.Embed(color=0xEF2AEF)

        # set all parameters for the embed
        embedVar.title = RequestDataResponse['global']['name'] + ' in BR ranked ' + RequestDataResponse['global']['rank']['rankedSeason']

        # create fields for infos
        if 'Apex Predator' == RequestDataResponse['global']['rank']['rankName']: # check for apex predator
            # change X1 platform to Xbox 1 of needed
            RequestDataResponse['global']['platform'] = RequestDataResponse['global']['platform'].replace('X1', 'Xbox 1')
            embedVar.add_field(name='Current Rank', value=RequestDataResponse['global']['rank']['rankName'] + ' #' + str(RequestDataResponse['global']['rank']['ladderPosPlatform']) + ' (' + str(RequestDataResponse['global']['platform']) + ')', inline=True)
        else:
            embedVar.add_field(name='Current Rank', value=RequestDataResponse['global']['rank']['rankName'] + ' #' + str(RequestDataResponse['global']['rank']['rankDiv']), inline=True)
        embedVar.add_field(name='Current RP', value=str(RequestDataResponse['global']['rank']['rankScore']) + ' RP', inline=True)

        # set thumbnail
        embedVar.set_thumbnail(url=str(RequestDataResponse['global']['rank']['rankImg']))

        # set footer and timestamp
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 
        embedVar.timestamp = datetime.datetime.now()

        # return embed
        return embedVar

    # configure embed for arena rank
    def ConfigEmbedAR(RequestDataResponse):
        # set color of embed
        embedVar = discord.Embed(color=0xEF2AEF)
        
        # set all parameters for the embed
        embedVar.title = RequestDataResponse['global']['name'] + ' in arenas ranked ' + RequestDataResponse['global']['arena']['rankedSeason']

        # create fields for infos
        embedVar.add_field(name='Current Rank', value=RequestDataResponse['global']['arena']['rankName'] + ' ' + str(RequestDataResponse['global']['arena']['rankDiv']), inline=True)
        embedVar.add_field(name='Current AP', value=str(RequestDataResponse['global']['arena']['rankScore']) + ' AP', inline=True)

        # set thumbnail
        embedVar.set_thumbnail(url=str(RequestDataResponse['global']['arena']['rankImg']))

        # set footer and timestamp
        embedVar.set_footer(text='Data from apexlegendsstatus.com') 
        embedVar.timestamp = datetime.datetime.now()

        # return embed
        return embedVar