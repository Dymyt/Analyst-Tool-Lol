#Copy file from the DONOTTOUCH FOLDER
from shutil import copyfile

#Write into an existing excel file
import xlwings
import variables as vars
import aux_functions as f

import datetime



#This function MODIFIES an excel template, adding various stats from different matches.
#FileName is the name of the excel file we are going to create. Matchobject list is a list of all the matches objects we would like to analyze,
#sideList are the sides where the team we are willing to analyze is playing.
#For accuracy the 5 players we are analysing in every game should be the same. This function does not admit "suplentes". ALWAYS the 5 same players :D.
def excelLeagueTeamStats(fileName, matchObjectsList, sideList):

    #Excel path from where we are copying the file
    excelPathTemplate =  vars.excelFilesDirectory + "DONOTTOUCH\TEAMLEAGUE_Template_donottouch.xlsx"
    #Excel path to save the file
    excelPath = vars.excelFilesDirectory + fileName + ".xlsx"

    #Copying excel template to proper folder
    copyfile(excelPathTemplate, excelPath)

    #OPEN EXCEL FILE AND ASSIGNING SHEETS
    excel = xlwings.Book(excelPath)
    DATA = excel.sheets[3]
    WARDING_DATA = excel.sheets[4]
    WRCHAMPS_DATA = excel.sheets[2]

    #WRITING IN EXCEL playerNames, TeamName..............
    player1Name = None
    player2Name = None
    player3Name = None
    player4Name = None
    player5Name = None
    team_Name = None

    if (sideList[0] == "BLUE"):
        player1Name= matchObjectsList[0].blueTeam.player1.summonerName
        player2Name= matchObjectsList[0].blueTeam.player2.summonerName
        player3Name= matchObjectsList[0].blueTeam.player3.summonerName
        player4Name= matchObjectsList[0].blueTeam.player4.summonerName
        player5Name= matchObjectsList[0].blueTeam.player5.summonerName
        team_Name = matchObjectsList[0].blueTeam.teamName
    else:
        player1Name= matchObjectsList[0].redTeam.player1.summonerName
        player2Name= matchObjectsList[0].redTeam.player2.summonerName
        player3Name= matchObjectsList[0].redTeam.player3.summonerName
        player4Name= matchObjectsList[0].redTeam.player4.summonerName
        player5Name= matchObjectsList[0].redTeam.player5.summonerName
        team_Name = matchObjectsList[0].redTeam.teamName

    DATA.range('E3').value = player1Name
    DATA.range('M3').value = player2Name
    DATA.range('U3').value = player3Name
    DATA.range('AC3').value = player4Name
    DATA.range('AK3').value = player5Name
    DATA.range('A1').value = team_Name

    #..............WRITING IN EXCEL playerNames, TeamName


    #WRITING IN EXCEL VARIOUS DATA FROM PLAYERS....................
    #CELL where the data from players starts
    ROW5 = 5
    COL5 = 5

    # CELL where the VISION data from players starts
    visionROW5 = 5
    visionCOL3 = 3

    # CELL where the champion DATA starts
    championDataROW5 = 5

    for match,side in zip(matchObjectsList,sideList):
        visioncolumn3 = visionCOL3
        column5 = COL5
        playersData = None
        enemyTeamName = None
        teamWin = None
        visionData = None
        allyTeamData = None
        enemyTeamData= None
        match_Duration = match.gameDuration
        champNamesList = None
        if side == "BLUE":
            playersData = match.blueTeam.playerStatsToList_dataSheet()
            enemyTeamName = match.redTeam.teamName
            teamWin = match.blueTeam.win
            visionData = match.blueTeam.playerVisionStatsToList_dataSheet()
            allyTeamData = match.blueTeam.teamStatsToList_dataSheet()
            enemyTeamData =match.redTeam.teamStatsToList_dataSheet()
            champNamesList = match.blueTeam.championNamesToList()
        else:
            playersData = match.redTeam.playerStatsToList_dataSheet()
            enemyTeamName = match.blueTeam.teamName
            teamWin = match.redTeam.win
            visionData = match.redTeam.playerVisionStatsToList_dataSheet()
            allyTeamData = match.redTeam.teamStatsToList_dataSheet()
            enemyTeamData = match.blueTeam.teamStatsToList_dataSheet()
            champNamesList = match.redTeam.championNamesToList()

        #WRITE SIDE, ENEMYTEAMNAME, WIN/LOSE
        DATA.range(ROW5, 2).value = side
        DATA.range(ROW5, 3).value = enemyTeamName
        DATA.range(ROW5, 4).value = teamWin

        #WRITE PLAYER DATA IN DATA SHEET
        for stat in playersData:
            DATA.range(ROW5, column5).value = stat
            column5 = column5 +1

        #WRITE MATCH DURATION, 50 is the position of the column in the data excel sheet we are willing to write in
        DATA.range(ROW5, 50).value = match_Duration

        #WRITE TEAM STATS IN DATA SHEET

        DATA.range(ROW5, 52).value = allyTeamData[0]
        DATA.range(ROW5, 53).value = allyTeamData[1]
        DATA.range(ROW5, 54).value = allyTeamData[2]
        DATA.range(ROW5, 55).value = allyTeamData[3]
        DATA.range(ROW5, 56).value = allyTeamData[4]
        DATA.range(ROW5, 63).value = allyTeamData[5]
        DATA.range(ROW5, 66).value = allyTeamData[6]
        DATA.range(ROW5, 69).value = allyTeamData[7]
        DATA.range(ROW5, 72).value = allyTeamData[8]
        DATA.range(ROW5, 73).value = allyTeamData[9]
        DATA.range(ROW5, 74).value = allyTeamData[10]
        DATA.range(ROW5, 75).value = allyTeamData[11]
        DATA.range(ROW5, 76).value = allyTeamData[12]

        # WRITE ENEMY TEAM STATS IN DATA SHEET

        DATA.range(ROW5, 57).value = enemyTeamData[0]
        DATA.range(ROW5, 58).value = enemyTeamData[1]
        DATA.range(ROW5, 59).value = enemyTeamData[2]
        DATA.range(ROW5, 60).value = enemyTeamData[3]
        DATA.range(ROW5, 61).value = enemyTeamData[4]
        DATA.range(ROW5, 64).value = enemyTeamData[5]
        DATA.range(ROW5, 67).value = enemyTeamData[6]
        DATA.range(ROW5, 70).value = enemyTeamData[7]

        #WRITE VISION PLATER DATA IN VISION DATA SHEET

        for stat in visionData:
            WARDING_DATA.range(visionROW5, visioncolumn3).value = stat
            visioncolumn3 = visioncolumn3 +1


        #NEXT MATCH STATS ARE GOING TO BE WRITTEN IN THE NEXT ROW
        ROW5 = ROW5 + 1
        visionROW5 = visionROW5 +1
        championDataROW5 = championDataROW5 + 1

    #WRITING IN CHAMPS WR DATA (LAST SHEET)
    dictionaryTOP, dictionaryJUN, dictionaryMID, dictionaryADC, dictionarySUP = f.champions_nMatches_Wins(matchObjectsList,sideList)

    #TOP
    WR_ROW5TOP = 5
    for champ, wrstats in zip(dictionaryTOP.keys(), dictionaryTOP.values()):
        WRCHAMPS_DATA.range(WR_ROW5TOP, 4).value = champ
        WRCHAMPS_DATA.range(WR_ROW5TOP, 5).value = wrstats[0]
        WRCHAMPS_DATA.range(WR_ROW5TOP, 6).value = wrstats[1]
        WR_ROW5TOP = WR_ROW5TOP +1

    #JUN
    WR_ROW5JUN = 5
    for champ, wrstats in zip(dictionaryJUN.keys(), dictionaryJUN.values()):
        WRCHAMPS_DATA.range(WR_ROW5JUN, 9).value = champ
        WRCHAMPS_DATA.range(WR_ROW5JUN, 10).value = wrstats[0]
        WRCHAMPS_DATA.range(WR_ROW5JUN, 11).value = wrstats[1]
        WR_ROW5JUN = WR_ROW5JUN +1

    #MID
    WR_ROW5MID = 5
    for champ, wrstats in zip(dictionaryMID.keys(), dictionaryMID.values()):
        WRCHAMPS_DATA.range(WR_ROW5MID, 14).value = champ
        WRCHAMPS_DATA.range(WR_ROW5MID, 15).value = wrstats[0]
        WRCHAMPS_DATA.range(WR_ROW5MID, 16).value = wrstats[1]
        WR_ROW5MID = WR_ROW5MID +1

    #ADC
    WR_ROW5ADC = 5
    for champ, wrstats in zip(dictionaryADC.keys(), dictionaryADC.values()):
        WRCHAMPS_DATA.range(WR_ROW5ADC, 19).value = champ
        WRCHAMPS_DATA.range(WR_ROW5ADC, 20).value = wrstats[0]
        WRCHAMPS_DATA.range(WR_ROW5ADC, 21).value = wrstats[1]
        WR_ROW5ADC = WR_ROW5ADC +1

    #SUP
    WR_ROW5SUP = 5
    for champ, wrstats in zip(dictionarySUP.keys(), dictionarySUP.values()):
        WRCHAMPS_DATA.range(WR_ROW5SUP, 24).value = champ
        WRCHAMPS_DATA.range(WR_ROW5SUP, 25).value = wrstats[0]
        WRCHAMPS_DATA.range(WR_ROW5SUP, 26).value = wrstats[1]
        WR_ROW5SUP = WR_ROW5SUP +1


    #....................WRITING IN EXCEL VARIOUS DATA FROM PLAYERS

    #Saving the excel file
    excel.save()
    excel.close()



#This function creates and modifies and excel template, adding various stats from diferent games from the same player.
#The excel file is divided in 6 sheets, being the last 4 places where we introduce data.

def excelPlayerStats(summonerName, initialDate, period1, period2, period3, period4):
    #Excel path from where we are copying the file
    excelPathTemplate =  vars.excelFilesDirectory + "DONOTTOUCH\PLAYER_Template_donottouch.xlsx"

    #Excel path to save the file
    excelPath = vars.excelFilesDirectory + summonerName + "_" + initialDate + ".xlsx"

    #Copying excel template to proper folder
    copyfile(excelPathTemplate, excelPath)

    #OPEN EXCEL FILE AND ASSIGNING SHEETS
    excel = xlwings.Book(excelPath)
    dataSheetPlayerStats = excel.sheets[0]
    dataSheetChampsWR = excel.sheets[1]
    dataSheetPeriod1 = excel.sheets[2]
    dataSheetPeriod2 = excel.sheets[3]
    dataSheetPeriod3 = excel.sheets[4]
    dataSheetPeriod4 = excel.sheets[5]


    dataSheetPlayerStats.range(1,1).value = summonerName + " EVOL. STATS"

    dataSheetPlayerStats.range(43,1).value = summonerName + " VISION EVOL. STATS"

    #WRITING INTO DATASHEETPERIOD1
    #Checking if the value is empty to avoid errors
    if len(period1) > 0:
        # SUMMONER NAME:
        dataSheetPeriod1.range("G1").value = summonerName
        # DATE TO DATE:
        dataSheetPeriod1.range("G3").value = str(datetime.datetime.strptime(initialDate, "%d-%m-%Y")) + "- - -" + str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=7))
        #StartingRowData
        startingRowData1 = 5
        for playerStatsInOneGame in period1:
            #WIN/LOSE
            dataSheetPeriod1.range(startingRowData1, 2).value = playerStatsInOneGame[0]
            #CHAMPION
            dataSheetPeriod1.range(startingRowData1, 4).value = playerStatsInOneGame[1]
            #ENEMYCHAMPION
            dataSheetPeriod1.range(startingRowData1, 6).value = playerStatsInOneGame[2]
            #KILLS
            dataSheetPeriod1.range(startingRowData1, 7).value = playerStatsInOneGame[3]
            #DEATHS
            dataSheetPeriod1.range(startingRowData1, 8).value = playerStatsInOneGame[4]
            #ASSISTS
            dataSheetPeriod1.range(startingRowData1, 9).value = playerStatsInOneGame[5]
            #CS
            dataSheetPeriod1.range(startingRowData1, 10).value = playerStatsInOneGame[6]
            #CS dif @ 15
            dataSheetPeriod1.range(startingRowData1, 11).value = playerStatsInOneGame[7]
            #DMG
            dataSheetPeriod1.range(startingRowData1, 12).value = playerStatsInOneGame[8]
            #DMG%
            dataSheetPeriod1.range(startingRowData1, 13).value = playerStatsInOneGame[9]
            #GOLD
            dataSheetPeriod1.range(startingRowData1, 14).value = playerStatsInOneGame[10]
            #GOLDDIF@15
            dataSheetPeriod1.range(startingRowData1, 15).value = playerStatsInOneGame[11]
            #GOLD%
            dataSheetPeriod1.range(startingRowData1, 16).value = playerStatsInOneGame[12]
            #DTIME
            dataSheetPeriod1.range(startingRowData1, 17).value = playerStatsInOneGame[13]
            #WARDS
            dataSheetPeriod1.range(startingRowData1, 19).value = playerStatsInOneGame[14]
            dataSheetPeriod1.range(startingRowData1, 20).value = playerStatsInOneGame[15]
            dataSheetPeriod1.range(startingRowData1, 21).value = playerStatsInOneGame[16]

            startingRowData1 = startingRowData1 + 1

    # WRITING INTO DATASHEETPERIOD2
    # Checking if the value is empty to avoid errors
    if len(period2) > 0:
        # SUMMONER NAME:
        dataSheetPeriod2.range("G1").value = summonerName
        # DATE TO DATE:
        dataSheetPeriod2.range("G3").value = str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=7)) + "- - -" + str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=14))
        # StartingRowData
        startingRowData1 = 5
        for playerStatsInOneGame in period2:
            # WIN/LOSE
            dataSheetPeriod2.range(startingRowData1, 2).value = playerStatsInOneGame[0]
            # CHAMPION
            dataSheetPeriod2.range(startingRowData1, 4).value = playerStatsInOneGame[1]
            # ENEMYCHAMPION
            dataSheetPeriod2.range(startingRowData1, 6).value = playerStatsInOneGame[2]
            # KILLS
            dataSheetPeriod2.range(startingRowData1, 7).value = playerStatsInOneGame[3]
            # DEATHS
            dataSheetPeriod2.range(startingRowData1, 8).value = playerStatsInOneGame[4]
            # ASSISTS
            dataSheetPeriod2.range(startingRowData1, 9).value = playerStatsInOneGame[5]
            # CS
            dataSheetPeriod2.range(startingRowData1, 10).value = playerStatsInOneGame[6]
            # CS dif @ 15
            dataSheetPeriod2.range(startingRowData1, 11).value = playerStatsInOneGame[7]
            # DMG
            dataSheetPeriod2.range(startingRowData1, 12).value = playerStatsInOneGame[8]
            # DMG%
            dataSheetPeriod2.range(startingRowData1, 13).value = playerStatsInOneGame[9]
            # GOLD
            dataSheetPeriod2.range(startingRowData1, 14).value = playerStatsInOneGame[10]
            # GOLDDIF@15
            dataSheetPeriod2.range(startingRowData1, 15).value = playerStatsInOneGame[11]
            # GOLD%
            dataSheetPeriod2.range(startingRowData1, 16).value = playerStatsInOneGame[12]
            # DTIME
            dataSheetPeriod2.range(startingRowData1, 17).value = playerStatsInOneGame[13]
            # WARDS
            dataSheetPeriod2.range(startingRowData1, 19).value = playerStatsInOneGame[14]
            dataSheetPeriod2.range(startingRowData1, 20).value = playerStatsInOneGame[15]
            dataSheetPeriod2.range(startingRowData1, 21).value = playerStatsInOneGame[16]

            startingRowData1 = startingRowData1 + 1

    # WRITING INTO DATASHEETPERIOD3
    # Checking if the value is empty to avoid errors
    if len(period3) > 0:
        # SUMMONER NAME:
        dataSheetPeriod3.range("G1").value = summonerName
        # DATE TO DATE:
        dataSheetPeriod3.range("G3").value = str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=14)) + "- - -" + str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=21))
        # StartingRowData
        startingRowData1 = 5
        for playerStatsInOneGame in period3:
            # WIN/LOSE
            dataSheetPeriod3.range(startingRowData1, 2).value = playerStatsInOneGame[0]
            # CHAMPION
            dataSheetPeriod3.range(startingRowData1, 4).value = playerStatsInOneGame[1]
            # ENEMYCHAMPION
            dataSheetPeriod3.range(startingRowData1, 6).value = playerStatsInOneGame[2]
            # KILLS
            dataSheetPeriod3.range(startingRowData1, 7).value = playerStatsInOneGame[3]
            # DEATHS
            dataSheetPeriod3.range(startingRowData1, 8).value = playerStatsInOneGame[4]
            # ASSISTS
            dataSheetPeriod3.range(startingRowData1, 9).value = playerStatsInOneGame[5]
            # CS
            dataSheetPeriod3.range(startingRowData1, 10).value = playerStatsInOneGame[6]
            # CS dif @ 15
            dataSheetPeriod3.range(startingRowData1, 11).value = playerStatsInOneGame[7]
            # DMG
            dataSheetPeriod3.range(startingRowData1, 12).value = playerStatsInOneGame[8]
            # DMG%
            dataSheetPeriod3.range(startingRowData1, 13).value = playerStatsInOneGame[9]
            # GOLD
            dataSheetPeriod3.range(startingRowData1, 14).value = playerStatsInOneGame[10]
            # GOLDDIF@15
            dataSheetPeriod3.range(startingRowData1, 15).value = playerStatsInOneGame[11]
            # GOLD%
            dataSheetPeriod3.range(startingRowData1, 16).value = playerStatsInOneGame[12]
            # DTIME
            dataSheetPeriod3.range(startingRowData1, 17).value = playerStatsInOneGame[13]
            # WARDS
            dataSheetPeriod3.range(startingRowData1, 19).value = playerStatsInOneGame[14]
            dataSheetPeriod3.range(startingRowData1, 20).value = playerStatsInOneGame[15]
            dataSheetPeriod3.range(startingRowData1, 21).value = playerStatsInOneGame[16]

            startingRowData1 = startingRowData1 + 1

    # WRITING INTO DATASHEETPERIOD4
    # Checking if the value is empty to avoid errors
    if len(period4) > 0:
        # SUMMONER NAME:
        dataSheetPeriod4.range("G1").value = summonerName
        # DATE TO DATE:
        dataSheetPeriod4.range("G3").value = str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=21)) + "- - -" + str(datetime.datetime.strptime(initialDate, "%d-%m-%Y") + datetime.timedelta(days=28))
        # StartingRowData
        startingRowData1 = 5
        for playerStatsInOneGame in period4:
            # WIN/LOSE
            dataSheetPeriod4.range(startingRowData1, 2).value = playerStatsInOneGame[0]
            # CHAMPION
            dataSheetPeriod4.range(startingRowData1, 4).value = playerStatsInOneGame[1]
            # ENEMYCHAMPION
            dataSheetPeriod4.range(startingRowData1, 6).value = playerStatsInOneGame[2]
            # KILLS
            dataSheetPeriod4.range(startingRowData1, 7).value = playerStatsInOneGame[3]
            # DEATHS
            dataSheetPeriod4.range(startingRowData1, 8).value = playerStatsInOneGame[4]
            # ASSISTS
            dataSheetPeriod4.range(startingRowData1, 9).value = playerStatsInOneGame[5]
            # CS
            dataSheetPeriod4.range(startingRowData1, 10).value = playerStatsInOneGame[6]
            # CS dif @ 15
            dataSheetPeriod4.range(startingRowData1, 11).value = playerStatsInOneGame[7]
            # DMG
            dataSheetPeriod4.range(startingRowData1, 12).value = playerStatsInOneGame[8]
            # DMG%
            dataSheetPeriod4.range(startingRowData1, 13).value = playerStatsInOneGame[9]
            # GOLD
            dataSheetPeriod4.range(startingRowData1, 14).value = playerStatsInOneGame[10]
            # GOLDDIF@15
            dataSheetPeriod4.range(startingRowData1, 15).value = playerStatsInOneGame[11]
            # GOLD%
            dataSheetPeriod4.range(startingRowData1, 16).value = playerStatsInOneGame[12]
            # DTIME
            dataSheetPeriod4.range(startingRowData1, 17).value = playerStatsInOneGame[13]
            # WARDS
            dataSheetPeriod4.range(startingRowData1, 19).value = playerStatsInOneGame[14]
            dataSheetPeriod4.range(startingRowData1, 20).value = playerStatsInOneGame[15]
            dataSheetPeriod4.range(startingRowData1, 21).value = playerStatsInOneGame[16]

            startingRowData1 = startingRowData1 + 1

    #WRITING IN CHAMP WR SHEET
    champsPlayedOrder = f.championsPlayed(period1, period2, period3, period4)
    rowStartChampWRData = 5
    for champ in champsPlayedOrder:
        dataSheetChampsWR.range(rowStartChampWRData, 4).value = champ[0]
        dataSheetChampsWR.range(rowStartChampWRData, 5).value = champ[1]
        rowStartChampWRData = rowStartChampWRData + 1



    #Saving the excel file
    excel.save()
    excel.close()

