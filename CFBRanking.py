import wget
import datetime
import os
import json
import pprint

# Set data file
now = datetime.datetime.now()

date = now.strftime("%Y-%m-%d")

DataFile = ('Data_File' + str(date) + '.data')

running = True
# Read user input

while running:
    print('##########################',)
    print('Options:','\n')
    print('1: (re) Import Data')
    print('2: Parse Data')
    print('3: Get Team Data')
    print('99: Exit')
    print('##########################','\n')
    option = int(input('Select Option Now:   '))
##################################################################################
    if option == 1:
        if os.path.exists(DataFile):
            print('### Replacing old file','\n')
            os.remove(DataFile)
        print('### Importing data')
        url = 'https://api.collegefootballdata.com/games?year=2018&seasonType=regular'
        GameData = wget.download(url, DataFile)
        print('\n','\n','### Import Complete')
# error handling for option != 1 but no file exists.
    if option != 1:
        no_file = True
        if os.path.exists(DataFile):
            no_file = False
            GameData = DataFile
        while no_file:
            if os.path.exists(DataFile):
                no_file = False
            else:
                no_file = True
                print('File',DataFile,'does not exist.','\n')
                DataFile = str(input('Input data file name:'))
##################################################################################
    if option == 2:
        with open(DataFile) as read_tmp1:
            read_tmp2 = json.load(read_tmp1)
            ParsedGameData = read_tmp2  # this is a list of dictionaries
#        print(type(ParsedGameData))
        pp = pprint.PrettyPrinter(indent=4)
#        pp.pprint(ParsedGameData[0])
        for read_tmp3 in ParsedGameData:
            pp.pprint(read_tmp3)
##################################################################################
    if option == 3:
        try:
            ParsedGameData
        except NameError:
            print('### Error: Data must be parsed before performing operations!','\n')
        else:
            TeamName_opt3 = str(input('Enter Team Name:  '))
            print('##########################','\n')
            for opt3_tmp1 in ParsedGameData:
                home_team = opt3_tmp1.get("home_team")
                away_team = opt3_tmp1.get("away_team")
                home_score = opt3_tmp1.get("home_points")
                away_score = opt3_tmp1.get("away_points")
                if home_team == TeamName_opt3 or away_team == TeamName_opt3:
                    print(home_team,home_score,away_team,away_score)

#                pp.pprint(ParsedGameData[games])
##################################################################################
# EXIT
##################################################################################

    if option == 99:
        running = False
        print('##########################',)
        print('####    Go Gators!!    ###')
        print('##########################',)

