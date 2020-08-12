import aux_functions as f
import variables as vars

#This package is to check if we already have the json files in our folder and do not make extra request to the RIOT API
import os.path
#This package is to connect to the RIOT API
import requests
#This package is to save files as json
import json
#This package is for delays
import time

#..............................END OF IMPORTS.................................................


#This function takes idMatch as input and generates two JSON files: idMatchGameSummary.json and idMatchTimeLine.json. This files are saved in the directory specified in variables.py
#This function also return the directory path of both files
#This function avoid extra requests to RIOT GAMES API
def getMatch(idMatch):

    #Defining where the JSON files are going to be saved and their file names
    pathGameSummary = vars.jsonDataDirectory + str(idMatch) + "GameSummary.json"
    pathTimeLine = vars.jsonDataDirectory + str(idMatch) +"TimeLine.json"

    #Checking if the file already exist to avoid extra request to RIOT GAMES
    #If the file does not exist a request is sent to RIOT API
    if (os.path.isfile(pathGameSummary) and os.path.isfile(pathTimeLine)):
        pass
    else:
        pass
        print ("............................Sending GAMESUMMARY Request to Riot Games...")
        #Building the Query for the GAMESUMMARY request (the query structure can be found on (https://developer.riotgames.com/apis#match-v4/GET_getMatch)
        gameSummaryQUERY = vars.matchRequestFirstPart + str (idMatch) + "?api_key=" + vars.APIKEY
        gameSummaryREQUEST = requests.get(gameSummaryQUERY)
        print("............................Sending TimeLine Request to Riot Games...")
        timeLineQUERY = vars.timeLineRequestFirstPart + str (idMatch) + "?api_key=" + vars.APIKEY
        timeLineREQUEST = requests.get(timeLineQUERY)

        #Checking if the GAMESUMMARY request was successful
        try:
            if (str(gameSummaryREQUEST) == "<Response [200]>"):
                print("Receiving correct answer from RIOT GAMES about GAME SUMMARY", str(gameSummaryREQUEST), "................")
                with open(pathGameSummary, "w") as outfile:
                    json.dump(gameSummaryREQUEST.json(), outfile)
            else:
                print("ERROR GAME SUMMARY: ", str(gameSummaryREQUEST), ".............", "go to: https://developer.riotgames.com/docs/portal")
        except ValueError:
            pass

        #Checking if the TIMELINE request was successful
        try:
            if (str(timeLineREQUEST) == "<Response [200]>"):
                print("Receiving correct answer from RIOT GAMES about TIME LINE", str(timeLineREQUEST), "................")
                with open(pathTimeLine, "w") as outfile:
                    json.dump(timeLineREQUEST.json(), outfile)
            else:
                print("ERROR TIMELINE: ", str(timeLineREQUEST), ".............", "go to: https://developer.riotgames.com/docs/portal")
        except ValueError:
            pass


    return pathGameSummary, pathTimeLine


#This function does the same as getMatch(), but with tournament server matches. It requires 2 extra parameters: server and gameHash.
#This function does not request anything to Riot Games with our API KEY
#This function needs a cookie Token in order to work (save the cookie token in variables.py). Further explanation in variables.py.
def getMatchTournament(idMatch, server, gameHash):

    #Defining where the JSON files are going to be saved and their file names
    pathGameSummary = vars.jsonDataDirectory + "TSERVER" + str(idMatch) + "GameSummary.json"
    pathTimeLine = vars.jsonDataDirectory + "TSERVER "+ str(idMatch) +"TimeLine.json"

    # Checking if the file already exist to avoid extra request to RIOT GAMES
    # If the file does not exist a request is sent to RIOT API
    if (os.path.isfile(pathGameSummary) and os.path.isfile(pathTimeLine)):
        pass
    else:
        print("............................Checking URL for Tournament Match...")
        #Building the URL for the GAMESUMMARY request (Server, idMatch, gameHash can be found in LEAGUEPEDIA -> LEAGUE WE ARE LOOKING FOR -> MATCH HISTORY)
        gameSummaryURL = "https://acs.leagueoflegends.com/v1/stats/game/" + server + "/" + idMatch + "?gameHash="  + gameHash
        gameSummaryREQUEST = requests.get(gameSummaryURL, cookies = vars.cookies)
        # Checking if the GAMESUMMARY request was successful
        try:
            if (str(gameSummaryREQUEST) == "<Response [200]>"):
                print("It was possible to access the URL for GAME SUMMARY", str(gameSummaryREQUEST),
                      "................")
                with open(pathGameSummary, "w") as outfile:
                    json.dump(gameSummaryREQUEST.json(), outfile)
            else:
                print("ERROR GAME SUMMARY: ", str(gameSummaryREQUEST), ".............",
                      "go to: https://developer.riotgames.com/docs/portal")
        except ValueError:
            pass
        # Building the URL for the TIMELINE request (Server, idMatch, gameHash can be found in LEAGUEPEDIA -> LEAGUE WE ARE LOOKING FOR -> MATCH HISTORY)
        timeLineURL = "https://acs.leagueoflegends.com/v1/stats/game/" + server + "/" + idMatch + "/timeline?gameHash="  + gameHash
        timeLineREQUEST = requests.get(timeLineURL, cookies = vars.cookies)

        #Checking if the TIMELINE request was successful
        try:
            if (str(timeLineREQUEST) == "<Response [200]>"):
                print("It was possible to access the URL for TIME LINE", str(timeLineREQUEST), "................")
                with open(pathTimeLine, "w") as outfile:
                    json.dump(timeLineREQUEST.json(), outfile)
            else:
                print("ERROR TIMELINE: ", str(timeLineREQUEST), ".............", "go to: https://developer.riotgames.com/docs/portal")
        except ValueError:
            pass
    return pathGameSummary, pathTimeLine


#This function takes two json filen and transform them into an match object (which is composed from team objects and player objects). It returns the match object.
def createMatchObject (gameSummaryPath, timeLinePath):
    #The two files are opened and saved in gameSummary and timeLine variables.
    with open(gameSummaryPath) as json_file:
        gameSummary = json.load(json_file)
    with open(timeLinePath) as json_file:
        timeLine = json.load(json_file)

    #Creation of the 10 player objects in a Match.
    playerList = []
    for indiceParticipante in range(10):
        playerList.append(f.createPlayerObject(gameSummary,timeLine,indiceParticipante))
    #Here the players are separated into blue and red and sorted by position
    bluePlayerList = f.getPlayerListSorted(playerList[:5])
    redPlayerList = f.getPlayerListSorted(playerList[5:])
    #Creation of every team object, assigning its players.
    blueTeam = f.createTeamObject(gameSummary,timeLine, 0, bluePlayerList)
    redTeam = f.createTeamObject(gameSummary, timeLine, 1, redPlayerList)

    #Creation of the match object, assigning its teams
    matchObject = f.createMatch(gameSummary, blueTeam, redTeam)

    return matchObject


#If the document name stars with with T_ it means is a tournament server match, if it begins with with N_ it means is a normal match from the day-to-day client.
#It returns two variables: 1.-List with all matches. 2.-List with all sides the team we are willing to analyze.
def generateTeamListMatchClass(textFileName):
    #Generating path to the file
    textFilePath = vars.textFilesDirectory + textFileName
    #Open, read the file and create a list with the separate lines.
    textFile = open(textFilePath, "r")
    linesInTextFile = textFile.read().splitlines()

    #Checking if is a tournament server match or a normal match to use one or another function.
    listMatchObjects = []
    side = []
    if textFileName[0] == "T" and textFileName[1] == "_":
        listMatchObjects, side = f.generateTeamListMatchClassTournamentServer(linesInTextFile)
    elif textFileName[0] == "N" and textFileName[1] == "_":
        listMatchObjects, side = f.generateTeamListMatchClassNormalServer(linesInTextFile)

    textFile.close()

    return listMatchObjects, side


#With a summoner name and an initial date, this function returns all...........
def generatePlayerListMatchClass (summonerName, initialDate):
    encryptedNameId = f.getSummonerID(summonerName)
    epochDateList = f.datesList(initialDate)

    period1 = []
    period2 = []
    period3 = []
    period4 = []
    #Checking how many dates the list have in order to do the proper operations:
    if len(epochDateList) == 1 or len(epochDateList) == 1:
        pass
    elif len(epochDateList) == 2:
        matchList1Week, championList1Week = f.getMatchList(encryptedNameId, epochDateList[0], epochDateList[1])
        period1 = f.matchListToPlayerStatList(matchList1Week, championList1Week)
    elif len(epochDateList) == 3:
        matchList1Week, championList1Week = f.getMatchList(encryptedNameId, epochDateList[0], epochDateList[1])
        period1 = f.matchListToPlayerStatList(matchList1Week, championList1Week)
        #DELAY.
        print ("waiting for big delay...", vars.bigDelay, "s")
        time.sleep(vars.bigDelay)
        matchList2Week, championList2Week = f.getMatchList(encryptedNameId, epochDateList[1], epochDateList[2])
        period2 = f.matchListToPlayerStatList(matchList2Week, championList2Week)
    elif len (epochDateList) == 4:
        matchList1Week, championList1Week = f.getMatchList(encryptedNameId, epochDateList[0], epochDateList[1])
        period1 = f.matchListToPlayerStatList(matchList1Week, championList1Week)
        #DELAY.
        print ("waiting for big delay...", vars.bigDelay, "s")
        time.sleep(vars.bigDelay)
        matchList2Week, championList2Week = f.getMatchList(encryptedNameId, epochDateList[1], epochDateList[2])
        period2 = f.matchListToPlayerStatList(matchList2Week, championList2Week)
        #DELAY.
        print ("waiting for big delay...", vars.bigDelay, "s")
        time.sleep(vars.bigDelay)
        matchList3Week, championList3Week = f.getMatchList(encryptedNameId, epochDateList[2], epochDateList[3])
        period3 = f.matchListToPlayerStatList(matchList3Week, championList3Week)
    elif len(epochDateList) == 5:
        matchList1Week, championList1Week = f.getMatchList(encryptedNameId, epochDateList[0], epochDateList[1])
        period1 = f.matchListToPlayerStatList(matchList1Week, championList1Week)
        #DELAY.
        print ("waiting for big delay...", vars.bigDelay, "s")
        time.sleep(vars.bigDelay)
        matchList2Week, championList2Week = f.getMatchList(encryptedNameId, epochDateList[1], epochDateList[2])
        period2 = f.matchListToPlayerStatList(matchList2Week, championList2Week)
        #DELAY.
        print ("waiting for big delay...", vars.bigDelay, "s")
        time.sleep(vars.bigDelay)
        matchList3Week, championList3Week = f.getMatchList(encryptedNameId, epochDateList[2], epochDateList[3])
        period3 = f.matchListToPlayerStatList(matchList3Week, championList3Week)
        #DELAY.
        print ("waiting for big delay...", vars.bigDelay, "s")
        time.sleep(vars.bigDelay)
        matchList4Week, championList4Week = f.getMatchList(encryptedNameId, epochDateList[3], epochDateList[4])
        period4 = f.matchListToPlayerStatList(matchList4Week, championList4Week)
    else:
        print("Something went wrong getting MATCH LISTS")

    #BORRAR ASTERISCOS
    return period1, period2, period3, period4