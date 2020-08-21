import functions
import excel_functions
import aux_functions



matchesList, sidesList= functions.generateTeamListMatchClass("N_KIWIS_30Junio.txt")




excel_functions.excelLeagueTeamStats("KiwisScrims30Junio", matchesList, sidesList)


aux_functions.champions_nMatches_Wins(matchesList,sidesList)