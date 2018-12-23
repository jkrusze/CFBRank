import wget
import datetime
import os
import json
import pprint
import numpy
import csv
##################################################################################
##################################################################################
################                     FUNCTIONS                   #################
##################################################################################
##################################################################################
def get_data(data_type,selected_team):
    if (print_get_data == 1):
        print('\n')
        print('### Getting Data')
        print('Getting stas for: ', selected_team)
    if data_type == 1:
        if os.path.exists(DataFile):
            print('### Replacing old file','\n')
            os.remove(DataFile)
        print('### Importing data')
        url = 'https://api.collegefootballdata.com/games?year=2018&seasonType=regular'
        GameData = wget.download(url, DataFile)
    if data_type == 2:
        selected_team2 = selected_team.replace(" ","%20")
        selected_team2 = selected_team2.replace("&","%26")
        selected_team2 = selected_team2.replace("Jose","Jos%C3%A9")
        selected_team2 = selected_team2.replace("José","Jos%C3%A9")
        if os.path.exists(DataFile):
            if (print_get_data == 1):
                print('### Replacing old file','\n')
            os.remove(DataFile)
        if (print_get_data == 1):
            print('### Importing data')
        url = 'https://api.collegefootballdata.com/games/teams?year=2018&seasonType=regular&team='+selected_team2
        GameData = wget.download(url, DataFile)
##################################################################################
##################################################################################
def parse_data(data_type):
    print('\n')
    if (print_get_data == 1):
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
def get_season_avg(selected_team, ParsedGameData):
    s_stats = [0] * 21
    opponent_list = [str('--')] * 21
    tmp6=0
    for tmp1 in ParsedGameData:
        tmp2=tmp1['teams']
        FBS_team=True
        for tmp3 in tmp2:
            if str(tmp3['conference']) == 'None':
                FBS_team=False
        if FBS_team:
            for tmp3 in tmp2:
                if tmp3['school'] == selected_team:
                    s_stats[1]=s_stats[1]+1
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
                        if tmp5['category'] == 'rushingAttempts':
                            s_stats[18]=s_stats[18]+int(tmp5['stat'])
                        if tmp5['category'] == 'completionAttempts':
                            tmp20 = tmp5['stat'].split('-')
                            s_stats[20] = s_stats[20] + int(tmp20[1])
                else:
                    opponent_list[tmp6]=tmp3['school']
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
    s_stats[1]=s_stats[1]-1 # Fucking 0-level indexing....
    return s_stats, opponent_list
##################################################################################
def get_opp_adj_data(selected_team):
# This function gets season data for each of the selected_teams's opponents.
# Data is then stored in opp_stats (internal only)
# Values calculated:
#
# oyppa_tot = the sum of the averages of Opponent Yards Per Pass Attempt
# oypra_tot = the sum of the averages of Opponent Yards Per Rush Attempt
# aoyppa = (passed on)the average of all oponents' oyppa_tot
# aoypra = (passed on)the average of all oponents' oypra_tot
# tot_att = total number of attempts
# fra_att_r = fraction of attempts which are rushing attempts
# fra_att_p = fraction of attempts which are passing attempts
# pts_p_a = (passed on) the points scored per yard, no matter how the yard is gained.
#   this is calculated by taking the points/game and dividing it by yards per play (total).
#   The second step requires weighing the yards per pass/rush attempt by the number
#   plays a team runs that is passing/rushing.
#
    if (print_get_data == 1):
        print('Selected team = ',selected_team)
    get_data(2,selected_team)
    ParsedGameData = parse_data(2)
    s_stats, opp_list = get_season_avg(selected_team, ParsedGameData)
    opp_stats = numpy.zeros((15,21))
    for x in range(0,s_stats[1]):
        if opp_list[x] != '--':
            selected_team = opp_list[x]
            get_data(2,selected_team)
            ParsedGameData = parse_data(2)
            os_stats, o_opp_list = get_season_avg(selected_team, ParsedGameData)
            opp_stats[x] = os_stats
        else:
            print("They ain't playyyd nobodyyy PAWWWLL")

    oyppa_tot=0
    oypra_tot=0
    o_games_tot=0
    for x in range (0,s_stats[1]):
        oyppa_tot = oyppa_tot + opp_stats[x,12]/opp_stats[x,1]
        oypra_tot = oypra_tot + opp_stats[x,8]/opp_stats[x,1]
    aoyppa = oyppa_tot / s_stats[1]
    aoypra = oypra_tot / s_stats[1]
#
    tot_att = s_stats[18]+s_stats[20]  # total number of play attempts
    fra_att_r = s_stats[18] / tot_att  # fraction of plays which are rushing
    fra_att_p = s_stats[20] / tot_att  # fraction of plays which are passing
    pts_p_a = (s_stats[2])/((s_stats[8]*fra_att_r+s_stats[12]*fra_att_p)) # points per attempt/yard.
#
    return s_stats, aoyppa, aoypra,  fra_att_r, fra_att_p, pts_p_a

##################################################################################
def team_matchup(selected_team1,selected_team2):
# This function calcualtes the matchup between two teams. It takes in the
# season average defenses for pass and rush (%) and weigth's the
# opponent's offense against it.
#
        s_stats1, aoyppa1, aoypra1, fra_att_r_1, fra_att_p_1,  pts_p_a1 = get_opp_adj_data(selected_team1)
        s_stats2, aoyppa2, aoypra2, fra_att_r_2, fra_att_p_2,  pts_p_a2 = get_opp_adj_data(selected_team2)
#
        frac_ra1 = ((s_stats1[9]/s_stats1[1])/aoypra1)  # Rush defense, team 1
        frac_pa1 = ((s_stats1[13]/s_stats1[1])/aoyppa1) # Pass defense, team 1
        frac_ra2 = ((s_stats2[9]/s_stats2[1])/aoypra2)  # Rush defense, team 2
        frac_pa2 = ((s_stats2[13]/s_stats2[1])/aoyppa2) # Pass defense, team 2
#
        pred_ypra1 = (s_stats1[8]/s_stats1[1]) * frac_ra2   #rush offense, team 1
        pred_yppa1 = (s_stats1[12]/s_stats1[1]) * frac_pa2  #pass offense, team 1
        pred_ypra2 = (s_stats2[8]/s_stats2[1]) * frac_ra1   #rush offense, team 2
        pred_yppa2 = (s_stats2[12]/s_stats2[1]) * frac_pa1  #pass offense, team 2
#
        pred_ypplay1 = pred_ypra1 * fra_att_r_1 + pred_yppa1 * fra_att_p_1
        pred_ypplay2 = pred_ypra2 * fra_att_r_2 + pred_yppa2 * fra_att_p_2
        pred_pts1 = pred_ypplay1 * pts_p_a1
        pred_pts2 = pred_ypplay2 * pts_p_a2

        return s_stats1, s_stats2, aoyppa1, aoypra1, aoyppa2, aoypra2, pred_yppa1, pred_ypra1, pred_yppa2, pred_ypra2, pred_ypplay1, pred_ypplay2, pred_pts1, pred_pts2

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
    print('5: Match Up Two Teams')
    print('6: Get Wins Predictions for a Team')
    print('99: Exit')
    print('##########################','\n')
    option = int(input('Select Option Now:   '))
    print_get_data = 1
##################################################################################
    if option == 1:
#        get_data(1,'Florida')
#        ParsedGameData=parse_data(1)
        TeamName_opt1 = 'Florida'
        while TeamName_opt1 != '99':
            print('\n','Type "99" to return to main menu','\n')
            TeamName_opt1 = str(input('Enter Team Name:  '))
            if TeamName_opt1 != '99':
                get_data(1,'TeamName_opt1')
                ParsedGameData=parse_data(1)
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
        s_stats, opp_list = get_season_avg(selected_team,ParsedGameData)
        print('\n')
        print('##########################','\n')
        print('FBS Opponents Played:')
        for x in range(0,s_stats[1]):
            print(opp_list[x])

        print('\n')
        print('Total # of Games:', s_stats[1],'\n')
        print('Points Scored Per Game:', round(s_stats[2]/s_stats[1],2), '   Points Given Up Per Game:', round(s_stats[3]/s_stats[1],2),'\n')
        print('Rushing Yards Per Game:', round(s_stats[10]/s_stats[1],2), 'Rushing Yards Per Allowed Game:', round(s_stats[11]/s_stats[1],2),'\n')
        print('AVG. Rushing Yards Per Attempt:', round(s_stats[8]/s_stats[1],2), 'AVG. Rushing Yards Per Attempt Allowed:', round(s_stats[9]/s_stats[1],2),'\n')
        print('Passing Yards Per Game:', round(s_stats[14]/s_stats[1],2), 'Passing Yards Allowed Game:', round(s_stats[15]/s_stats[1],2),'\n')
        print('AVG. Passing Yards Per Attempt:', round(s_stats[12]/s_stats[1],2), 'AVG. Passinging Yards Per Attempt Allowed:', round(s_stats[13]/s_stats[1],2),'\n')
        print('First Downs per Game:', round(s_stats[16]/s_stats[1],2), 'First Downs per Game Allowed:', round(s_stats[17]/s_stats[1],2),'\n')
        print('AVG. Fumbles Won:', round(s_stats[7]/s_stats[1],2), 'AVG. Fumbles Lost:', round(s_stats[6]/s_stats[1],2),'\n')
        print('AVG. Interceptions Won:', round(s_stats[5]/s_stats[1]), 'AVG. Interceptions Lost:', round(s_stats[4]/s_stats[1],2),'\n')


##################################################################################
    if option == 4:
        selected_team4 = str(input('Enter Team Name:  '))

        s_stats, aoyppa, aoypra, fra_att_r, fra_att,  pts_p_a = get_opp_adj_data(selected_team4)

        print('Passing Allowed % =',round((s_stats[13]*100/s_stats[1])/aoyppa,3))
        print('Rushing Allowed % =',round((s_stats[9]*100/s_stats[1])/aoypra,3))
        print('AVG. Rushing Yards Per Attempt:', round(s_stats[8]/s_stats[1],2), 'AVG. Rushing Yards Per Attempt Allowed:', round(s_stats[9]/s_stats[1],2),'\n')
        print('AVG. Passing Yards Per Attempt:', round(s_stats[12]/s_stats[1],2), 'AVG. Passinging Yards Per Attempt Allowed:', round(s_stats[13]/s_stats[1],2),'\n')

##################################################################################

    if option == 5:

        selected_team1 = str(input('Enter Name of Team 1 :  '))
        print('\n')
        selected_team2 = str(input('Enter Name of Team 2 :  '))

        s_stats1, s_stats2, aoyppa1, aoypra1, aoyppa2, aoypra2, pred_yppa1, pred_ypra1, pred_yppa2, pred_ypra2, pred_ypplay1, pred_ypplay2, pred_pts1, pred_pts2 = team_matchup(selected_team1,selected_team2)

        print('\n')
        print('\n')
        print(selected_team1)
        print('Passing Allowed % =',round((s_stats1[13]*100/s_stats1[1])/aoyppa1,3))
        print('Rushing Allowed % =',round((s_stats1[9]*100/s_stats1[1])/aoypra1,3))
        print('Predicted Yards Per Pass Attempt =',round(pred_yppa1, 3))
        print('Predicted Yards Per Rush Attempt =',round(pred_ypra1, 3))
        print('Predicted Yards Per Play =',round(pred_ypplay1, 3))
        print('Predicted Points Scored =',round(pred_pts1, 3))
        print('\n')
        print('\n')
        print(selected_team2)
        print('Passing Allowed % =',round((s_stats2[13]*100/s_stats2[1])/aoyppa2,3))
        print('Rushing Allowed % =',round((s_stats2[9]*100/s_stats2[1])/aoypra2,3))
        print('Predicted Yards Per Pass Attempt =',round(pred_yppa2, 3))
        print('Predicted Yards Per Rush Attempt =',round(pred_ypra2, 3))
        print('Predicted Yards Per Play =',round(pred_ypplay2, 3))
        print('Predicted Points Scored =',round(pred_pts2, 3))
        print('\n')
        print('\n')

##################################################################################

    if option == 6:
        selected_team1 = str(input('Enter Name of the Team  :  '))
        print_get_data = int(input('Print Intermediate Output? 1 = yes, 0 = no  :  '))
#       read list of FBS teams from file
        with open('ListOfFBSSchools.csv', 'r') as FBSFile:
            reader = csv.reader(FBSFile)
            FBSList = list(reader)
# Convert to list of strings
        FBSList = list(map(''.join,FBSList))
#
        pts_for_tot = 0
        pts_aga_tot = 0
        tot_wins = 0
        count = 0
        for opponent in FBSList:
            count = count + 1
            print ('Now Doing Team',count,'/130')
            if (selected_team1 != opponent):
                s_stats1, s_stats2, aoyppa1, aoypra1, aoyppa2, aoypra2, pred_yppa1, pred_ypra1, pred_yppa2, pred_ypra2, pred_ypplay1, pred_ypplay2, pred_pts1, pred_pts2 = team_matchup(selected_team1,opponent)
                pts_for_tot = pred_pts1 + pts_for_tot
                pts_aga_tot = pred_pts2 + pts_aga_tot
                if (pred_pts1 > pred_pts2):
                    tot_wins = tot_wins+1
            else:
                print('Skipping:', opponent)

        print('Total points for:', pts_for_tot)
        print('Total points against:', pts_aga_tot)
        print('Total wins:', tot_wins,'out of',count)










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

