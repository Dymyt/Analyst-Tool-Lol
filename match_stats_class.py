
#This class stores all the stats from two teams in a match :D
#.............INCLUIR UN SET para incluir el cambio de nombre de un gameNAME
class match:
    def __init__(self, idMatch, blueTeam, redTeam, gameDuration, gameName = "NOGAMENAME"):
        self.idMatch = idMatch
        self.blueTeam = blueTeam
        self.redTeam = redTeam
        self.gameDuration = float(gameDuration) / 60.0
        self.gameName = gameName


