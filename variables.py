#Here we store all the final variables that we use across the code

#WRITE HERE YOUR API_KEY. you should register and request one->(https://developer.riotgames.com/)
APIKEY = "" 

#First part of the QUERY to get the GAMESUMMARY JSON file in EUWest server
matchRequestFirstPart = "https://euw1.api.riotgames.com/lol/match/v4/matches/"
#First part of the QUERY to get the Game Time Line JSON file in EUWest server
timeLineRequestFirstPart = "https://euw1.api.riotgames.com/lol/match/v4/timelines/by-match/"


#First part of the QUERY to get the account encrypted ID from a summoner name
encryptedIDQUERY = r'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'


#First part of the QUERY to get a list of matches from a player between 2 dates
matchListQUERY = r'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/'


#.......HERE IS DEFINED WHERE TO SAVE JSON FILES AND EXCEL FILES.........
#You have to create an empty folder called 'analystData' and three subfolders inside called 'excelFiles', 'textFiles' and 'jsonData' in C: (Windows).
#You can change the name of the folder and the path of them changing the values of the following variables.
rootDirectory = r"C:\analystData\\"
excelFilesDirectory = rootDirectory + r"excelFiles\\"
jsonDataDirectory = rootDirectory + r"jsonData\\"
textFilesDirectory = rootDirectory + r"textFiles\\"
#..............................................................



#In order to access match stats from the tournament server we need to be logged in LoleSports. Once we are logged press F12->go to Storage->Cookies->id_token
#Copy the id_token in cookies value
cookies = {'id_token': 'include here your token'}


#Dictionary with every champion and his number
dicChamp = {'266': 'Aatrox', '103': 'Ahri', '84': 'Akali', '12': 'Alistar', '32': 'Amumu', '34': 'Anivia', '1': 'Annie',
                '523': 'Aphelios', '22': 'Ashe', '136': 'AurelionSol', '268': 'Azir', '432': 'Bard', '53': 'Blitzcrank', '63': 'Brand',
                '201': 'Braum', '51': 'Caitlyn', '164': 'Camille', '69': 'Cassiopeia', '31': "Chogath", '42': 'Corki', '122': 'Darius',
                '131': 'Diana', '119': 'Draven', '36': 'DrMundo', '245': 'Ekko', '60': 'Elise', '28': 'Evelynn', '81': 'Ezreal', '9': 'Fiddlesticks',
                '114': 'Fiora', '105': 'Fizz', '3': 'Galio', '41': 'Gangplank', '86': 'Garen', '150': 'Gnar', '79': 'Gragas', '104': 'Graves',
                '120': 'Hecarim', '74': 'Heimerdinger', '420': 'Illaoi', '39': 'Irelia', '427': 'Ivern', '40': 'Janna', '59': 'JarvanIV', '24': 'Jax',
                '126': 'Jayce', '202': 'Jhin','222': 'Jinx', '145': "Kaisa", '429': 'Kalista', '43': 'Karma', '30': 'Karthus', '38': 'Kassadin',
                '55': 'Katarina', '10': 'Kayle', '141': 'Kayn', '85': 'Kennen', '121': "Khazix", '203': 'Kindred', '240': 'Kled', '96': "KogMaw",
                '7': 'Leblanc', '64': 'LeeSin', '89': 'Leona', '127': 'Lissandra', '236': 'Lucian', '117': 'Lulu', '99': 'Lux', '54': 'Malphite',
                '90': 'Malzahar', '57': 'Maokai', '11': 'MasterYi', '21': 'MissFortune', 'g': 'MonkeyKing', '82': 'Mordekaiser', '25': 'Morgana',
                '267': 'Nami', '75': 'Nasus','111': 'Nautilus', '518': 'Neeko', '76': 'Nidalee', '56': 'Nocturne', '20': 'Nunu', '2': 'Olaf',
                '61': 'Orianna', '516': 'Ornn', '80': 'Pantheon', '78': 'Poppy', '555': 'Pyke', '246': 'Qiyana', '133': 'Quinn', '497': 'Rakan',
                '33': 'Rammus', '421': "RekSai", '58': 'Renekton', '107': 'Rengar', '92': 'Riven', '68': 'Rumble', '13': 'Ryze', '113': 'Sejuani',
                '235': 'Senna', '875': 'Sett', '35': 'Shaco', '98': 'Shen', '102': 'Shyvana', '27': 'Singed', '14': 'Sion', '15': 'Sivir', '72': 'Skarner',
                '37': 'Sona','16': 'Soraka', '50': 'Swain', '517': 'Sylas', '134': 'Syndra', '223': 'TahmKench', '163': 'Taliyah', '91': 'Talon',
                '44': 'Taric', '17': 'Teemo', '412': 'Thresh', '18': 'Tristana', '48': 'Trundle', '23': 'Tryndamere', '4': 'TwistedFate', '29': 'Twitch',
                '77': 'Udyr', '6': 'Urgot', '110': 'Varus', '67': 'Vayne', '45': 'Veigar', '161': "Velkoz", '254': 'Vi', '112': 'Viktor', '8': 'Vladimir',
                '106': 'Volibear', '19': 'Warwick', '498': 'Xayah', '101': 'Xerath', '5': 'XinZhao', '157': 'Yasuo', '83': 'Yorick', '350':'Yuumi',
                '154': 'Zac', '238': 'Zed', '115': 'Ziggs', '26': 'Zilean', '142': 'Zoe', '143': 'Zyra', '62': 'MonkeyKing', '-1': 'No ban'}

dicPosition = {1: "TOP", 2: "JUN", 3: "MID", 4: "ADC", 5: "SUP"}

#Delay between RIOT API REQUEST (set to 0 if you get a production key).
delay = 0.5
bigDelay = 10
