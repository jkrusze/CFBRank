import wget
import datetime
import os
import json
import pprint
import numpy
##################################################################################
##################################################################################
################                     FUNCTIONS                   #################
##################################################################################
##################################################################################
def get_data(data_type,TeamName):
    print('\n')
    print('### Getting Data')
    if data_type == 1:
        if os.path.exists(DataFile):
            print('### Replacing old file','\n')
            os.remove(DataFile)
        print('### Importing data')
        url = 'https://api.collegefootballdata.com/games?year=2018&seasonType=regular'
        GameData = wget.download(url, DataFile)
    if data_type == 2:
        TeamName_opt2 = TeamName.replace(" ","%20")
        if os.path.exists(DataFile):
            print('### Replacing old file','\n')
            os.remove(DataFile)
        print('### Importing data')
        url = 'https://api.collegefootballdata.com/games/teams?year=2018&seasonType=regular&team='+TeamName_opt2
        GameData = wget.download(url, DataFile)
##################################################################################
##################################################################################
def parse_data(data_type):
    print('\n')
    print('### Parsing Data')
    if data_type == 1:
        with open(DataFile) as read_tmp1:
            read_tmp2 = json.load(read_tmp1)
            ParsedGameData = read_tmp2  # this is a list of dictionaries
            return ParsedGameData
    if data_type == 2:
        with open(DataFile) as read_tmp1:
            read_tmp2 = json.load(read_tmp1)
            ParsedGameData = read_tmp2  # this is a list of dictionaries
#            print(type(ParsedGameData))
#            pp = pprint.PrettyPrinter(indent=4)
#            pp.pprint(ParsedGameData)
#        for read_tmp3 in ParsedGameData:
#            pp.pprint(read_tmp3)
            return ParsedGameData
##################################################################################
def get_season_avg(selected_team):
    s_stats = [0] * 18
    opponent_list = [str('--')] * 18
    tmp6=0
    print('FBS Opponents for', selected_team)
    for tmp1 in ParsedGameData:
        tmp2=tmp1['teams']
        FBS_team=True
        for tmp3 in tmp2:
            if str(tmp3['conference']) == 'None':
                FBS_team=False
        if FBS_team:
            for tmp3 in tmp2:
                print('win #',s_stats[1])
                s_stats[1]=s_stats[1]+1
                if tmp3['school'] == selected_team:
                    tmp4=tmp3['stats']
                    s_stats[2]=s_stats[2]+tmp3['points']
                    for tmp5 in tmp4:
                        if tmp5['category'] == 'interceptions':
                            s_stats[4]=s_stats[4]+int(tmp5['stat'])
                        if tmp5['category'] == 'fumblesLost':
                                s_stats[6]=s_stats[6]+int(tmp5['stat'])
                        if tmp5['category'] == 'yardsPerRushAttempt':
                            s_stats[8]=s_stats[8]+float(tmp5['stat'])
                        if tmp5['category'] == 'rushingYards':
                            s_stats[10]=s_stats[10]+float(tmp5['stat'])
                        if tmp5['category'] == 'yardsPerPass':
                            s_stats[12]=s_stats[12]+float(tmp5['stat'])
                        if tmp5['category'] == 'netPassingYards':
                            s_stats[14]=s_stats[14]+float(tmp5['stat'])
                        if tmp5['category'] == 'firstDowns':
                            s_stats[16]=s_stats[16]+int(tmp5['stat'])
                else:
                    opponent_list[tmp6]=tmp3['school']
                    print('Opponent:',tmp3['school'],'Conference:',tmp3['conference'])
                    tmp6=tmp6+1
                    tmp4=tmp3['stats']
                    s_stats[3]=s_stats[3]+int(tmp3['points'])
                    for tmp5 in tmp4:
                        if tmp5['category'] == 'interceptions':
                            s_stats[5]=s_stats[5]+int(tmp5['stat'])
                        if tmp5['category'] == 'fumblesLost':
                            s_stats[7]=s_stats[7]+int(tmp5['stat'])
                        if tmp5['category'] == 'yardsPerRushAttempt':
                            s_stats[9]=s_stats[9]+float(tmp5['stat'])
                        if tmp5['category'] == 'rushingYards':
                            s_stats[11]=s_stats[11]+float(tmp5['stat'])
                        if tmp5['category'] == 'yardsPerPass':
                            s_stats[13]=s_stats[13]+float(tmp5['stat'])
                        if tmp5['category'] == 'netPassingYards':
                            s_stats[15]=s_stats[15]+float(tmp5['stat'])
                        if tmp5['category'] == 'firstDowns':
                            s_stats[17]=s_stats[17]+int(tmp5['stat'])
    return s_stats, opponent_list
##################################################################################
# Set data file
now = datetime.datetime.now()

date = now.strftime("%Y-%m-%d")

DataFile = ('Data_File' + str(date) + '.data')

running = True
# Read user input
while running:
    print('##########################',)
    print('Options:','\n')
    print('1: Get Season Records')
    print('2: Get Detailed Stats for a Team')
    print('3: Get Team Season Averages')
    print('4: Get Opponent-Adjusted Stats')
    print('99: Exit')
    print('##########################','\n')
    option = int(input('Select Option Now:   '))
##################################################################################
    if option == 1:
        get_data(1,'Florida')
        ParsedGameData=parse_data(1)
        TeamName_opt1 = 'Florida'
        while TeamName_opt1 != '99':
            print('\n','Type "99" to return to main menu','\n')
            TeamName_opt1 = str(input('Enter Team Name:  '))
            if TeamName_opt1 != 'BACK':
                for opt1_tmp1 in ParsedGameData:
                 home_team = opt1_tmp1.get("home_team")
                 away_team = opt1_tmp1.get("away_team")
                 home_score = opt1_tmp1.get("home_points")
                 away_score = opt1_tmp1.get("away_points")
                 if home_team == TeamName_opt1 or away_team == TeamName_opt1:
                     print(home_team,home_score,away_team,away_score)
##################################################################################
    if option == 2:
        TeamName_opt2 = str(input('Enter Team Name:  '))
        get_data(2,TeamName_opt2)
        ParsedGameData=parse_data(2)
        WhichWeek=1
        for games in ParsedGameData:
            print('##########################','\n')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(ParsedGameData)
##################################################################################
    if option == 3:

        selected_team = str(input('Enter Team Name:  '))
        get_data(2,selected_team)
        ParsedGameData = parse_data(2)
        s_stats, opp_list = get_season_avg(selected_team)

        print('\n')
        print('##########################','\n')
        print('Total # of Games:', s_stats[1],'\n')
        print('Points Scored Per Game:', round(s_stats[2]/s_stats[1],2), '   Points Given Up Per Game:', round(s_stats[3]/s_stats[1],2),'\n')
        print('Rushing Yards Per Game:', round(s_stats[10]/s_stats[1],2), 'Rushing Yards Allowed Game:', round(s_stats[11]/s_stats[1],2),'\n')
        print('AVG. Rushing Yards Per Attempt:', round(s_stats[8]/s_stats[1],2), 'AVG. Rushing Yards Per Attempt Allowed:', round(s_stats[9]/s_stats[1],2),'\n')
        print('Passing Yards Per Game:', round(s_stats[14]/s_stats[1],2), 'Passing Yards Allowed Game:', round(s_stats[15]/s_stats[1],2),'\n')
        print('AVG. Passing Yards Per Attempt:', round(s_stats[12]/s_stats[1],2), 'AVG. Passinging Yards Per Attempt Allowed:', round(s_stats[13]/s_stats[1],2),'\n')
        print('First Downs per Game:', round(s_stats[16]/s_stats[1],2), 'First Downs per Game Allowed:', round(s_stats[17]/s_stats[1],2),'\n')
        print('AVG. Fumbles Won:', round(s_stats[7]/s_stats[1],2), 'AVG. Fumbles Lost:', round(s_stats[6]/s_stats[1],2),'\n')
        print('AVG. Interceptions Won:', round(s_stats[5]/s_stats[1]), 'AVG. Interceptions Lost:', round(s_stats[4]/s_stats[1],2),'\n')


##################################################################################
    if option == 4:
        selected_team = str(input('Enter Team Name:  '))
        get_data(2,selected_team)
        ParsedGameData = parse_data(2)
        s_stats, opp_list = get_season_avg(selected_team)
        opp_stats = numpy.zeros((18,s_stats[1]))
        print('s_Stats[1]=',s_stats[0])
        for x in range(0,s_stats[0]):
            if opp_list[x] != '--':
                print(x)
                print(opp_list[x])
                selected_team = opp_list[x]
                get_data(2,selected_team)
                ParsedGameData = parse_data
            else:
                print("They ain't playyyd nobodyyy PAWWWELLL")
                # opp_stats[x], opp_opp_list = get_season_avg(selected_team)
        #print(opp_stats)




##################################################################################

#                pp.pprint(ParsedGameData[games])
##################################################################################
# EXIT
##################################################################################
    if option == 99:
        running = False
        print('##########################',)
        print('####    Go Gators!!    ###')
        print('##########################',)

