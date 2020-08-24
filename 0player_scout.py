import aux_functions
import functions
import excel_functions

period1, period2, period3, period4 = functions.generatePlayerListMatchClass("Devyluke", "01-07-2020")

print(period1, period2, period3, period4)

print(aux_functions.championsPlayed(period1, period2, period3, period4))

excel_functions.excelPlayerStats("Devyluke", "01-07-2020", period1, period2, period3, period4)
