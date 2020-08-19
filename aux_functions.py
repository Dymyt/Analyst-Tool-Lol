import player_stats_class as playerClass
import team_stats_class as teamClass
import match_stats_class as matchClass
import functions as mainf
import variables as vars
#For delay module
import time
#For doing calculations with dates
import datetime
import requests
import json

#To check champions played
from collections import Counter

#This function takes two json files and extract all the stats from the player[index] creating the player object. returns a player object
def createPlayerObject(gameSummary, timeLine, index):

    #Getting info from the JSON DOCUMENT GAME SUMMARY
    matchID = gameSummary["gameId"]
    date = gameSummary ["gameCreation"]
    gameDuration = gameSummary["gameDuration"]
    champion = gameSummary["participants"][index]["championId"]

    #SINCE stats field has too many information we use the following thing for easyreading purposes
    stats = gameSummary["participants"][index]["stats"]

    kills = stats["kills"]
    deaths = stats["deaths"]
    assists = stats["assists"]
    totalDamageDealtToChampions = stats["totalDamageDealtToChampions"]
    totalDamageTaken = stats["totalDamageTaken"]
    totalHeal = stats["totalHeal"]
    totalTimeCrowdControlDealt = stats["totalTimeCrowdControlDealt"]
    visionScore = stats["visionScore"]
    visionWardsBoughtInGame = stats["visionWardsBoughtInGame"]
    wardsPlaced = stats["wardsPlaced"]
    wardsKilled = stats["wardsKilled"]
    goldEarned = stats["goldEarned"]
    #totalminionsKilled is CS + jungle monsters. Pretty obvious :D.
    totalMinionsKilled = int(stats["totalMinionsKilled"] + stats["neutralMinionsKilled"])
    neutralMinionsKilledTeamJungle = stats["neutralMinionsKilledTeamJungle"]
    neutralMinionsKilledEnemyJungle = stats["neutralMinionsKilledEnemyJungle"]
    damageDealtToObjectives = stats["damageDealtToObjectives"]
    damageDealtToTurrets = stats["damageDealtToTurrets"]
    turretKills = stats["turretKills"]
    inhibitorKills = stats["inhibitorKills"]

    #This attribute is used for tracking purposes.
    participantId = gameSummary["participants"][index]["participantId"]


    GOLDDIF15, CSDIF15 = getGoldAndCsDif(timeLine, participantId)

    role = gameSummary["participants"][index]["timeline"]["role"]
    lane = gameSummary["participants"][index]["timeline"]["lane"]

    participantIdPosition = getPlayerPosition(timeLine, participantId)

    #Checking if the game is a personalized game. In this case we return 'PersonalizedGame' as summonerGame
    #When is a personalized game gameSummary["participantIdentities"][index]) only have one field.
    summonerName = "PersonalizedGame"
    if len(gameSummary["participantIdentities"][index]) > 1:
        summonerName = gameSummary["participantIdentities"][index]["player"]["summonerName"]

    win = stats["win"]

    playerObject = playerClass.player(matchID, date, gameDuration, champion, kills, deaths, assists, totalDamageDealtToChampions,
                                     totalDamageTaken, totalHeal, totalTimeCrowdControlDealt, visionScore, visionWardsBoughtInGame,
                                     wardsPlaced, wardsKilled, goldEarned, totalMinionsKilled, neutralMinionsKilledTeamJungle,
                                     neutralMinionsKilledEnemyJungle, damageDealtToObjectives, damageDealtToTurrets, turretKills,
                                     inhibitorKills, CSDIF15, GOLDDIF15, role, lane, participantId, participantIdPosition, summonerName)

    return playerObject


#This function is helping createPlayerObject to get the stats CSDIF at 15, and GOLDDIF at 15. How i did it:
#In timeLine the players are sorted out by top-jung-mid... we give to this function the json file time line and the participant ID of the player we want to know the stats.
#First we check in which position our player is playing, and we compare it with the player in the same position in the opposing team.
def getGoldAndCsDif (timeLine, participantId):
    CSDIF15 = 0
    GOLDDIF15 = 0
    indexPlayer = 0
    indexEnemy = 0
    #If the game is less than 15 minutes this part of the function do nothing.
    if len(timeLine["frames"]) < 16:
        pass
    else:
        playerTimeLine = timeLine["frames"][15]["participantFrames"]
        for i in range(1,11):
            if playerTimeLine[str(i)]["participantId"] == participantId:
                indexPlayer = i
                break
        if int(indexPlayer) > 5:
            indexEnemy = indexPlayer - 5
        else:
            indexEnemy = indexPlayer + 5

        GOLDDIF15 = playerTimeLine[str(indexPlayer)]["totalGold"] - playerTimeLine[str(indexEnemy)]["totalGold"]
        CSDIF15 = playerTimeLine[str(indexPlayer)]["minionsKilled"] + playerTimeLine[str(indexPlayer)]["jungleMinionsKilled"] - playerTimeLine[str(indexEnemy)]["minionsKilled"] - playerTimeLine[str(indexEnemy)]["jungleMinionsKilled"]

    return  GOLDDIF15,CSDIF15


#This function goes to the json timeLine file and check in which position the player is playing. It helps the function createPlayerObject (assigns a position :D)
#This gets the player position with a simple mapping, It can fail 12.5% of the times ->(https://riot-api-libraries.readthedocs.io/en/latest/roleid.html)
def getPlayerPosition (timeLine, participantId):
    indexPlayer = 0
    playerTimeLine = timeLine["frames"][0]["participantFrames"]
    for i in range(1, 11):
        if playerTimeLine[str(i)]["participantId"] == participantId:
            indexPlayer = i
            break
    if indexPlayer > 5:
        indexPlayer = indexPlayer - 5
    return indexPlayer


#This Aux function helps to sort a team of 5 players by position. It is used in functions->createMatchObject
def getPlayerListSorted(playerList):
    playerListSorted = [0,1,2,3,4]
    for p in playerList:
        if (p.participantIdPosition == "TOP"):
            playerListSorted[0] = p
        if (p.participantIdPosition == "JUN"):
            playerListSorted[1] = p
        if (p.participantIdPosition == "MID"):
            playerListSorted[2] = p
        if (p.participantIdPosition == "ADC"):
            playerListSorted[3] = p
        if (p.participantIdPosition == "SUP"):
            playerListSorted[4] = p
    return playerListSorted


#This function takes two json files, side of the team (0= blue, 1= red),and 5 players.
#It extracts all the stats from a team. returns a team object. this team objetct is compound of 5 player objects
def createTeamObject(gameSummary, timeLine, side, playerList):
    # Getting info from the JSON DOCUMENT GAME SUMMARY
    matchID = gameSummary["gameId"]
    teamSide = side

    #SINCE team stats field has too many information we use the following thing for easyreading purposes
    stats = gameSummary["teams"][side]

    win = stats["win"]
    firstBlood = stats["firstBlood"]
    firstTower = stats["firstTower"]
    firstInhibitor = stats["firstInhibitor"]
    firstBaron =  stats["firstBaron"]
    firstDragon = stats ["firstDragon"]
    firstRiftHerald = stats["firstRiftHerald"]
    towerKills = stats["towerKills"]
    inhibitorKills = stats["inhibitorKills"]
    baronKills= stats["baronKills"]
    dragonKills = stats["dragonKills"]
    riftHeraldKills = stats["riftHeraldKills"]

    #Here is used the aux function getDragonKills in order to set how many drake types the team has killed.
    dictDrakes =  getDragonKills(timeLine, side)
    oceanDrake = dictDrakes["WATER_DRAGON"]
    fireDrake = dictDrakes["FIRE_DRAGON"]
    earthDrake = dictDrakes["EARTH_DRAGON"]
    windDrake = dictDrakes["AIR_DRAGON"]
    elderDrake = dictDrakes["ELDER_DRAGON"]

    player1 = playerList[0]
    player2 = playerList[1]
    player3 = playerList[2]
    player4 = playerList[3]
    player5 = playerList[4]

    bans = []


    teamObject = teamClass.team(matchID, teamSide, win, firstBlood, firstTower, firstInhibitor, firstBaron, firstDragon, firstRiftHerald,
                                towerKills, inhibitorKills, baronKills, dragonKills, riftHeraldKills, oceanDrake, fireDrake, earthDrake,
                                windDrake, elderDrake, player1, player2, player3, player4, player5, bans)

    return teamObject


#This function gets how many kind of drakes each team has done. It is used in createTeamObject function.
def getDragonKills(timeLine, side):
    player1 = 1
    player5 = 5
    if side == 1:
        player1 = 6
        player5 = 10

    drakes = {"WATER_DRAGON":0, "FIRE_DRAGON": 0, "EARTH_DRAGON": 0, "AIR_DRAGON": 0, "ELDER_DRAGON": 0}
    for min in timeLine["frames"]:
        for event in min["events"]:
            if event["type"] == "ELITE_MONSTER_KILL":
                if event["monsterType"] == "DRAGON":
                    if event["killerId"]>= player1 and event["killerId"]<= player5:
                        drakes[event["monsterSubType"]] = drakes[event["monsterSubType"]] + 1
    return drakes


#This function takes two json files and two teams, with this it creates a match objects. Retrun the object.
def createMatch (gameSummary, bTeam, rTeam):
    matchID = gameSummary["gameId"]
    blueTeam = bTeam
    redTeam = rTeam
    gameDuration = gameSummary["gameDuration"]

    matchObject = matchClass.match(matchID, blueTeam, redTeam, gameDuration)

    return matchObject


#this function returns a list of match objects and a list with the sides where your team/the team you are analysing is playing.
def generateTeamListMatchClassTournamentServer(linesInTextFile):
    #Creating as many list as parameters our textfile has.
    idMatchList = []
    serverList = []
    gameHashList = []
    teamSide = []
    teamName = []
    enemyTeamName = []

    #adding to each list their values
    for line in linesInTextFile:
        idMatchList.append(line.split(", ")[0])
        serverList.append(line.split(", ")[1])
        gameHashList.append(line.split(", ")[2])
        teamSide.append(line.split(", ")[3])
        teamName.append(line.split(", ")[4])
        enemyTeamName.append(line.split(", ")[5])

    #list of matches, the one is going to be returned
    matchList = []

    #Downloading files from RIOT WEB, converting them into match objects, and appending every object to a list
    for i in range (len(idMatchList)):
        gameSummaryPath, timeLinePath = mainf.getMatchTournament(idMatchList[i], serverList[i], gameHashList[i])
        matchObject = mainf.createMatchObject(gameSummaryPath, timeLinePath)
        #set team names to the teams :D
        if teamSide[i] == "BLUE":
            matchObject.blueTeam.setTeamName(teamName[i])
            matchObject.redTeam.setTeamName(enemyTeamName[i])
        elif teamSide[i] == "RED":
            matchObject.blueTeam.setTeamName(enemyTeamName[i])
            matchObject.redTeam.setTeamName(teamName[i])
        matchList.append(matchObject)

        #.......To do not surpasse RIOT API LIMIT, take it away if you get a production KEY.........................
        time.sleep(vars.delay)

    return matchList, teamSide

#this function returns a list of match objects and a list with the sides where your team/the team you are analysing is playing.
def generateTeamListMatchClassNormalServer(linesInTextFile):
    idMatchList = []
    teamSide = []
    teamName = []
    enemyTeamName = []

    for line in linesInTextFile:
        idMatchList.append(line.split(", ")[0])
        teamSide.append(line.split(", ")[1])
        teamName.append(line.split(", ")[2])
        enemyTeamName.append(line.split(", ")[3])

    #list of matches, the one is going to be returned
    matchList = []

    #Downloading files from RIOT WEB, converting them into match objects, and appending every object to a list
    for i in range(len(idMatchList)):
        gameSummaryPath, timeLinePath = mainf.getMatch(idMatchList[i])
        matchObject = mainf.createMatchObject(gameSummaryPath, timeLinePath)
        # set team names to the teams :D
        if teamSide[i] == "BLUE":
            matchObject.blueTeam.setTeamName(teamName[i])
            matchObject.redTeam.setTeamName(enemyTeamName[i])
        elif teamSide[i] == "RED":
            matchObject.blueTeam.setTeamName(enemyTeamName[i])
            matchObject.redTeam.setTeamName(teamName[i])
        matchList.append(matchObject)

        # .......To do not surpasse RIOT API LIMIT, take it away if you get a production KEY.........................
        time.sleep(vars.delay)

    return matchList, teamSide


#giving a list of match objects and a sideList, this function return a dictionary with champion names, times these champion were played in the side specified and how many times this champ won.
def champions_nMatches_Wins (matchObjectsList, sideList):
    dictionaryTOP = {}
    dictionaryJUN = {}
    dictionaryMID = {}
    dictionaryADC = {}
    dictionarySUP = {}
    for match,side in zip(matchObjectsList,sideList):
        championNamesList = None
        if side == "BLUE":
            championNamesList = match.blueTeam.championNamesToList()
            teamWin = match.blueTeam.win
        else:
            championNamesList = match.redTeam.championNamesToList()
            teamWin = match.redTeam.win
        #TOP POSITION
        if championNamesList[0] not in dictionaryTOP:
            dictionaryTOP.update({championNamesList[0]: [1,0]})
            if teamWin == "WIN":
                dictionaryTOP[championNamesList[0]][1] = dictionaryTOP[championNamesList[0]][1] + 1
        else:
            dictionaryTOP[championNamesList[0]][0] = dictionaryTOP[championNamesList[0]][0] + 1
            if teamWin == "WIN":
                dictionaryTOP[championNamesList[0]][1] = dictionaryTOP[championNamesList[0]][1] + 1

        #JUN POSITION
        if championNamesList[1] not in dictionaryJUN:
            dictionaryJUN.update({championNamesList[1]: [1,0]})
            if teamWin == "WIN":
                dictionaryJUN[championNamesList[1]][1] = dictionaryJUN[championNamesList[1]][1] + 1
        else:
            dictionaryJUN[championNamesList[1]][0] = dictionaryJUN[championNamesList[1]][0] + 1
            if teamWin == "WIN":
                dictionaryJUN[championNamesList[1]][1] = dictionaryJUN[championNamesList[1]][1] + 1

        #MID POSITION
        if championNamesList[2] not in dictionaryMID:
            dictionaryMID.update({championNamesList[2]: [1,0]})
            if teamWin == "WIN":
                dictionaryMID[championNamesList[2]][1] = dictionaryMID[championNamesList[2]][1] + 1
        else:
            dictionaryMID[championNamesList[2]][0] = dictionaryMID[championNamesList[2]][0] + 1
            if teamWin == "WIN":
                dictionaryMID[championNamesList[2]][1] = dictionaryMID[championNamesList[2]][1] + 1

        #ADC POSITION
        if championNamesList[3] not in dictionaryADC:
            dictionaryADC.update({championNamesList[3]: [1,0]})
            if teamWin == "WIN":
                dictionaryADC[championNamesList[3]][1] = dictionaryADC[championNamesList[3]][1] + 1
        else:
            dictionaryADC[championNamesList[3]][0] = dictionaryADC[championNamesList[3]][0] + 1
            if teamWin == "WIN":
                dictionaryADC[championNamesList[3]][1] = dictionaryADC[championNamesList[3]][1] + 1

        #SUP POSITION
        if championNamesList[4] not in dictionarySUP:
            dictionarySUP.update({championNamesList[4]: [1,0]})
            if teamWin == "WIN":
                dictionarySUP[championNamesList[4]][1] = dictionarySUP[championNamesList[4]][1] + 1
        else:
            dictionarySUP[championNamesList[4]][0] = dictionarySUP[championNamesList[4]][0] + 1
            if teamWin == "WIN":
                dictionarySUP[championNamesList[4]][1] = dictionarySUP[championNamesList[4]][1] + 1

    return dictionaryTOP, dictionaryJUN, dictionaryMID, dictionaryADC, dictionarySUP


#Giving a beginning date this function will give a list of MAX 5 dates (one month). EX: giving 01/05/2020 the function will return:
#[01/05/2020, 07/05/2020, 14/05/2020, 21/05/2020, 28/05/2020]
#It will return less parameters if we get to actual date. #[01/05/2020, 07/05/2020, 14/05/2020, 17/05/2020] if we are in 17/05/2020 :D.
#This functions is used because we can only ask riot for 7 days period of ranked matches, not longer.
#It will return the dates in epoch ms

def datesList (dateNormal):
    listDatesEpoch = []
    date_1 = datetime.datetime.strptime(dateNormal, "%d-%m-%Y")
    date_2 = date_1 + datetime.timedelta(days=7)
    date_3 = date_2 + datetime.timedelta(days=7)
    date_4 = date_3 + datetime.timedelta(days=7)
    date_5 = date_4 + datetime.timedelta(days=7)

    #Today DATE to just cover till there.
    today = datetime.datetime.today()



    #We need to return an epoch date in ms (thats why the *1000) and it should be an integer value for riot API

    listDatesEpoch.append(int(date_1.timestamp() * 1000))

    if today > date_2:
        listDatesEpoch.append(int(date_2.timestamp() * 1000))
    if today> date_3:
        listDatesEpoch.append(int(date_3.timestamp() * 1000))
    if today > date_4:
        listDatesEpoch.append(int(date_4.timestamp() * 1000))
    if today > date_5:
        listDatesEpoch.append(int(date_5.timestamp() * 1000))

    if date_5 > today:
        listDatesEpoch.append(int(today.timestamp() * 1000))

    return listDatesEpoch


#This function connects with the Riot API and ask for the summoner account ID. It requires the summoner name.

def getSummonerID(summonerName):
    print ("Connecting with RIOT API... Asking for:", summonerName, " encrypted account ID.")

    query = vars.encryptedIDQUERY + summonerName + "?api_key=" + vars.APIKEY

    request = requests.get(query)

    if (str(request) == "<Response [200]>"):
        print ("RIOT API answered correctly: ", request)
        return request.json()["accountId"]
    else:
        print("¿?¿?¿?Something went wrong:", request)
        return "FAIL"


#This function returns a list with all the game's matchIDs x summoner has played between two dates. requires encrypted account ID, initial date and ending date.

def getMatchList (encryptedId, initialDateEpoch, endingDateEpoch):
    QUERY = vars.matchListQUERY + encryptedId + "?endTime=" +  str(endingDateEpoch) + "&beginTime=" + str(initialDateEpoch) + "&api_key=" + vars.APIKEY

    print ("Getting match list between", initialDateEpoch, "and", endingDateEpoch)
    request = requests.get(QUERY)
    if (str(request) == "<Response [200]>"):
        print ("RIOT API answered correctly: ", request)
        matchIdRankedGameList = []
        championPlayedList = []
        #We only get to the json file if there are some matches inside. We do this in order to avoid error.
        for matchDescription in request.json()["matches"]:
            if int(matchDescription["queue"]) == 440 or int(matchDescription["queue"]) == 420:
                matchIdRankedGameList.append(matchDescription["gameId"])
                champPlayed = vars.dicChamp[str(matchDescription["champion"])]
                championPlayedList.append(champPlayed)
    else:
        print("¿?¿?¿?Something went wrong:", request)

    return matchIdRankedGameList, championPlayedList


#Gives a list of lists with all the player stats we need to write in the proper excel file.

def matchListToPlayerStatList (matchIdList, championPlayedList):
    playerStatsList = []
    for matchId, championName in zip(matchIdList, championPlayedList):
        #Getting the json files
        gameSummary, timeLine = mainf.getMatch(matchId)
        #Creating the match object
        matchObject = mainf.createMatchObject(gameSummary, timeLine)
        print ("waiting for delay...", vars.delay, "s")
        #Delay to do not surpass RIOT API limit.
        time.sleep(vars.delay)
        playerStats = getPlayerStats(matchObject, championName)
        playerStatsList.append(playerStats)

    return playerStatsList


def getPlayerStats (matchObject, championName):
    blueTeam = matchObject.blueTeam
    statList = []
    redTeam = matchObject.redTeam

    blueIndex = 0
    for bluePlayer in blueTeam.getPlayers():
        if bluePlayer.champion == championName:
            statList = bluePlayer.statsToList_PlayerStatsExcel()
            win = blueTeam.win
            goldPor = blueTeam.goldPorcentage(bluePlayer.goldEarned)
            dmgPor = blueTeam.dmgPorcentage(bluePlayer.totalDamageDealtToChampions)
            enemyChampionName = redTeam.getPlayers()[blueIndex].champion
            statList.insert(0, win)
            statList.insert(2, enemyChampionName)
            statList.insert(9, dmgPor)
            statList.insert(12, goldPor)
            break
        blueIndex = blueIndex + 1
    redIndex = 0
    for redPlayer in redTeam.getPlayers():
        if redPlayer.champion == championName:
            statList = redPlayer.statsToList_PlayerStatsExcel()
            win = redTeam.win
            goldPor = redTeam.goldPorcentage(redPlayer.goldEarned)
            dmgPor = redTeam.dmgPorcentage(redPlayer.totalDamageDealtToChampions)
            enemyChampionName = blueTeam.getPlayers()[redIndex].champion
            statList.insert(0, win)
            statList.insert(2, enemyChampionName)
            statList.insert(9, dmgPor)
            statList.insert(12, goldPor)


            break
        redIndex = redIndex + 1

    return statList


#Return a order list with all the champs played in various periods. sort by times played. [('Ornn', 22), ('Maokai', 18), ('Zac', 9)...
def championsPlayed (period1, period2, period3, period4):
    listChamps = []
    if len(period1)>0:
        for playerStats in period1:
            listChamps.append(playerStats[1])
        if len(period2) > 0:
            for playerStats in period2:
                listChamps.append(playerStats[1])
            if len(period3) > 0:
                for playerStats in period3:
                    listChamps.append(playerStats[1])
                if len(period4) > 0:
                    for playerStats in period4:
                        listChamps.append(playerStats[1])
    dicChampPlayed = dict(Counter(listChamps))
    dicChampPlayedSorted = sorted(dicChampPlayed.items(), key =lambda  x: x[1], reverse=True)
    return dicChampPlayedSorted