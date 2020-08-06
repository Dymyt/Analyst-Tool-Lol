#This package is helping to transform from epoch ms to DD-MM-YYYY in the date attribute
import time
import variables as vars

#This class stores all the stats from a player in a match.
class player:
    def __init__(self, idMatch, date, gameDuration, champion, kills, deaths, assists, totalDamageDealtToChampions, totalDamageTaken,
                 totalHeal, totalTimeCrowdControlDealt, visionScore, visionWardsBoughtInGame, wardsPlaced, wardsKilled, goldEarned, totalMinionsKilled,
                 neutralMinionsKilledTeamJungle, neutralMinionsKilledEnemyJungle,damageDealtToObjectives,
                 damageDealtToTurrets, turretKills, inhibitorKills, CSDIF15, GOLDDIF15, role, lane, participantId, participantIdPosition, summonerName = "NoNameAvailable", win ="false"):
        self.idMatch = idMatch
        #Converting epoch time to DD MM YYYY
        self.date = time.strftime('%d/%m/%Y', time.gmtime(date/1000.0))
        #Converting number to actual champion name
        self.gameDuration = float(gameDuration) / 60.0
        self.champion = vars.dicChamp[str(champion)]
        self.kills = kills
        self.deaths = deaths
        self.assists =  assists
        self.totalDamageDealtToChampions = totalDamageDealtToChampions
        self.totalDamageTaken = totalDamageTaken
        self.totalHeal = totalHeal
        self.totalTimeCrowdControlDealt = totalTimeCrowdControlDealt
        self.visionScore = visionScore
        self.visionWardsBoughtInGame = visionWardsBoughtInGame
        self.wardsPlaced = wardsPlaced
        self.wardsKilled = wardsKilled
        self.goldEarned = goldEarned
        self.totalMinionsKilled = totalMinionsKilled
        self.neutralMinionsKilledTeamJungle = neutralMinionsKilledTeamJungle
        self.neutralMinionsKilledEnemyJungle = neutralMinionsKilledEnemyJungle
        self.damageDealtToObjectives = damageDealtToObjectives
        self.damageDealtToTurrets = damageDealtToTurrets
        self.turretKills = turretKills
        self.inhibitorKills = inhibitorKills
        self.CSDIF15 = CSDIF15
        self.GOLDDIF15 = GOLDDIF15
        self.role = role
        self.lane = lane
        self.participantId = participantId
        self.participantIdPosition = vars.dicPosition[participantIdPosition]
        self.summonerName = summonerName
        if bool(win):
            self.win = win
        else:
            self.win = "LOSE"
    #Print function to check everything is correct. You can delete this.
    def print (self):
        print ("*************")
        print ("NAME: " + self.summonerName+"(" + str(self.participantId) + ")" + " | DATE: " + str(self.date)
               + "| Game Duration: " + str(self.gameDuration) + "mins. | Champ (Lane): " + str(self.champion) + "("+ str(self.participantIdPosition) + ")"
               +" | KDA: " + str(self.kills) + "/" + str(self.deaths) + "/" + str(self.assists)
               + " | DMG to CHAMPS: " + str(self.totalDamageDealtToChampions) + " | DMG Received: " + str(self.totalDamageTaken)
               + " | Total Heal: " + str(self.totalHeal) + " | CC DONE: " + str(self.totalTimeCrowdControlDealt) +"\n"+
               "Vision Score: " + str(self.visionScore) + " | Control Wards: " + str(self.visionWardsBoughtInGame) + " | Wards Placed: "
               + str(self.wardsPlaced) + " | Wards destroyed: " + str(self.wardsKilled) + " | GOLD earned: " +
               str(self.goldEarned)+  "| CS total: " + str(self.totalMinionsKilled)  + " | CS DIF @ 15: " + str(self.CSDIF15) +
               " | GOLD DIF @ 15: "+ str(self.GOLDDIF15) + "\n" + "monster jungle/enemy jungle: " + str(self.neutralMinionsKilledTeamJungle) + "/"+
               str(self.neutralMinionsKilledEnemyJungle) + " | DMG to objetives: " + str(self.damageDealtToObjectives) + " | DMG to TOWERS: "+
               str(self.damageDealtToTurrets) + " | TOWERS DESTROYED : "+ str(self.turretKills)+ " | Inhibs. destroyed: " + str(self.inhibitorKills))
        print("*************")


    #This function return a list with all the parameters we need for the data sheet in the excel file
    def statsToList_dataSheet (self):
        return [int(self.kills), int(self.deaths), int(self.assists), int(self.totalMinionsKilled), int (self.CSDIF15), float(self.totalDamageDealtToChampions),
                float(self.goldEarned), float(self.GOLDDIF15)]


    def visionStatsToList_dataSheet (self):
        return [int(self.visionWardsBoughtInGame), int(self.wardsPlaced), int(self.wardsKilled)]

    #This function is used for getting the info we need for the player stats template. From an aux function we get DMG%, GOLD% and Enemy champion.
    def statsToList_PlayerStatsExcel (self):
        return [self.champion, self.kills, self.deaths, self.assists, self.totalMinionsKilled, self.CSDIF15, self.totalDamageDealtToChampions, self.goldEarned,
                self.GOLDDIF15, self.gameDuration, self.visionWardsBoughtInGame, self.wardsPlaced, self.wardsKilled]