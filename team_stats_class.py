import variables as vars

#This class stores the TEAM stats from a Match and the 5 players from the team.

class team:
    def __init__(self, matchID, teamSide, win, firstBlood, firstTower, firstInhibitor, firstBaron, firstDragon, firstRiftHerald,
            towerKills, inhibitorKills, baronKills, dragonKills, riftHeraldKills, oceanDrake, fireDrake, earthDrake, windDrake, elderDrake, player1 = None, player2 = None, player3 = None,
             player4 = None, player5 = None, bans = None, teamName = None):

        self.matchID = matchID
        self.teamSide = teamSide
        if(win == "Win"):
            self.win = "WIN"
        else:
            self.win = "LOSE"

        if firstBlood:
            self.firstBlood = 1
        else:
            self.firstBlood = 0

        if firstTower:
            self.firstTower = 1
        else:
            self.firstTower = 0

        if firstInhibitor:
            self.firstInhibitor = 1
        else:
            self.firstInhibitor = 0

        if firstBaron:
            self.firstBaron = 1
        else:
            self.firstBaron = 0

        if firstDragon:
            self.firstDragon = 1
        else:
            self.firstDragon = 0

        if firstRiftHerald:
            self.firstRiftHerald = 1
        else:
            self.firstRiftHerald = 0
        self.towerKills = towerKills
        self.inhibitorKills = inhibitorKills
        self.baronKills = baronKills
        self.dragonKills = dragonKills
        self.riftHeraldKills = riftHeraldKills
        self.oceanDrake = oceanDrake
        self.fireDrake = fireDrake
        self.earthDrake = earthDrake
        self.windDrake = windDrake
        self.elderDrake = elderDrake
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        #Converting bans list of champ-numbers into string separated bv "-" of champ-names
        self.bans =  self.bansList(bans)
        self.teamName = teamName


    def print(self):
        print ("^^^^^^")
        print ("TEAM SIDE (Blue:0, Red:1): " +  str(self.teamSide) + " | WIN?: " + str(self.win) + " | FirstBlood: " + str(self.firstBlood) + " | firstTower: " + str(self.firstTower)+
               " | firstInhibitor: " + str(self.firstInhibitor) + " | firstBaron: " + str(self.firstBaron) + " | firstDragon: " + str(self.firstDragon)+
               " | firstRiftHerald: " + str(self.firstRiftHerald) + "\ntowerKills: " + str(self.towerKills) + " | inhibitorKills: " + str(self.inhibitorKills)+
               " | Baron Kills: " + str(self.baronKills) + " | Herald Kills: " + str(self.riftHeraldKills) + " | Dragon Kills: " + str(self.dragonKills)+ " | OCEAN/FIRE/EARTH/WIND/ELDER DRAKE: " +
               str(self.oceanDrake) + "/" + str(self.fireDrake) + "/" + str(self.earthDrake) + "/" + str(self.windDrake) + "/" + str(self.elderDrake) +"\n"+
               "BANS: " + str(self.bans)+ " | TEAM NAME: " +  str(self.teamName) + " | TEAM SIDE: " + str(self.teamSide))
        print ("^^^^^^")


    #Aux function to convert the list of champ-number bans, into a string separeted with "-" of champ-names bans
    #EX: it will convert the list: [10,15,202,2,111] into the string: Soraka-Evelynn-Diana-Yasuo-Yuumi
    def bansList(self, bansList):
        lBans = []
        for c in bansList:
            lBans.append(vars.dicChamp[str(c)])
        sBans = "-".join(lBans)
        return sBans

    #Function to set a TeamName
    def setTeamName(self, name):
        self.teamName = name

    #Function to return players in a list.
    def getPlayers(self):
        return [self.player1, self.player2, self.player3, self.player4, self.player5]


    #It returns a LIST with all the data we need to introduce in the sheet DATA from our excel
    def playerStatsToList_dataSheet(self):
        statsList = []
        list1= self.player1.statsToList_dataSheet()
        list2= self.player2.statsToList_dataSheet()
        list3= self.player3.statsToList_dataSheet()
        list4= self.player4.statsToList_dataSheet()
        list5= self.player5.statsToList_dataSheet()
        statsList.extend(list1)
        statsList.extend(list2)
        statsList.extend(list3)
        statsList.extend(list4)
        statsList.extend(list5)

        return statsList

    #It returns a LIST with all the vision data we need to introduce in the sheet VISION DATA from our excel
    def playerVisionStatsToList_dataSheet(self):
        visionStatsList = []
        list1= self.player1.visionStatsToList_dataSheet()
        list2= self.player2.visionStatsToList_dataSheet()
        list3= self.player3.visionStatsToList_dataSheet()
        list4= self.player4.visionStatsToList_dataSheet()
        list5= self.player5.visionStatsToList_dataSheet()
        visionStatsList.extend(list1)
        visionStatsList.extend(list2)
        visionStatsList.extend(list3)
        visionStatsList.extend(list4)
        visionStatsList.extend(list5)

        return visionStatsList

    #Same as the one before but with vision.
    def teamStatsToList_dataSheet(self):
        return (self.windDrake, self.fireDrake, self.oceanDrake, self.earthDrake, self.elderDrake, self.baronKills, self.riftHeraldKills,
                self.towerKills, self.firstBlood, self.firstTower, self.firstDragon, self.firstRiftHerald, self.firstBaron)

    #Return a list with the champion names in order (TOP, JUN, MID...)

    def championNamesToList (self):
        return (self.player1.champion, self.player2.champion, self.player3.champion, self.player4.champion, self.player5.champion)


    #it's used to calculate how much % from a gold from a team a player has
    def goldPorcentage(self, gold):
        totalGold = int(self.player1.goldEarned) + int(self.player2.goldEarned) + int(self.player3.goldEarned) + int(self.player4.goldEarned) + int(self.player5.goldEarned)
        goldPor = float(gold / totalGold)
        return goldPor


    #it's used to calculate how much % from a DMG from a team a player has
    def dmgPorcentage(self, dmg):
        totalDmg = int(self.player1.totalDamageDealtToChampions) + int(self.player2.totalDamageDealtToChampions) + int(self.player3.totalDamageDealtToChampions) + int(self.player4.totalDamageDealtToChampions) + int(self.player5.totalDamageDealtToChampions)
        dmgPor = float(dmg / totalDmg)
        return dmgPor
