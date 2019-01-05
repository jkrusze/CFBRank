import wget
import datetime
import os
import json
import pprint
import numpy
import csv
import time
##################################################################################
##################################################################################
################                     FUNCTIONS                   #################
##################################################################################
##################################################################################
def pause():
    temp_pause = str(input('Paused. Press any key to continue...'))

##################################################################################
##################################################################################
def get_data(data_type,selected_team):
    global team_done, done_teams, get_talent
    if (print_get_data == 1):
        print('\n')
        print('### Getting Data')
        print('\n')
        print('Getting stats for: ', selected_team)
    if data_type == 1:
        if os.path.exists(DataFile):
            print('\n')
            print('### replacing old file','\n')
            os.remove(DataFile)
        print('\n')
        print('### Importing data')
        url = 'https://api.collegefootballdata.com/games?year=2018&seasonType=regular'
        GameData = wget.download(url, DataFile)
    if data_type == 2:
        if (get_talent == 1):
            if os.path.exists(TalentFile):
                print('### Replacing old talent file','\n')
                os.remove(TalentFile)
            print('### Getting New Talent file','\n')
            url = 'https://api.collegefootballdata.com/talent?year=2018'
            TalentData = wget.download(url,TalentFile)
            get_talent = 0
        team_done = selected_team
        if(selected_team in done_teams):
            if (print_get_data == 1):
                print('Data aquisition for',team_done,'is being skipped.')
        else:
            selected_team2 = selected_team.replace(" ","%20")
            selected_team2 = selected_team2.replace("&","%26")
            selected_team2 = selected_team2.replace("Jose","Jos%C3%A9")
            selected_team2 = selected_team2.replace("José","Jos%C3%A9")
            if os.path.exists(DataFile):
                if (print_get_data == 1):
                    print('### Replacing old file','\n')
                os.remove(DataFile)
            if (print_get_data == 1):
                print('\n')
                print('### Importing data')
            url = 'https://api.collegefootballdata.com/games/teams?year=2018&seasonType=regular&team='+selected_team2
            GameData = wget.download(url, DataFile)

##################################################################################
##################################################################################
def parse_data(data_type):
    global team_done, done_teams
    if (print_get_data == 1):
        print('\n')
        print('### Parsing Data')
    if data_type == 1:
        with open(DataFile) as read_tmp1:
            read_tmp2 = json.load(read_tmp1)
            ParsedGameData = read_tmp2  # this is a list of dictionaries
            return ParsedGameData
    if data_type == 2:
        if(team_done in done_teams):
            if (print_get_data == 1):
                print('Recovering old game data for',team_done)
            ParsedGameData = done_teams.get(team_done)
        else:
             with open(DataFile) as read_tmp1:
                read_tmp2 = json.load(read_tmp1)
                ParsedGameData = read_tmp2  # this is a list of dictionaries
                done_teams[team_done] = ParsedGameData
        with open(TalentFile) as read_tmp3:
            read_tmp4 = json.load(read_tmp3)
            ParsedTalentData = read_tmp4
#                 for team in ParsedTalentData:
#                     if (team.get('school') == team_done):
#                         print(team_done,' talent=', team.get('talent'))
#                 print(type(ParsedTalentData[1]))
#                 pp = pprint.PrettyPrinter(indent=4)
#                 pp.pprint(ParsedTalentData)
#        for read_tmp3 in ParsedGameData:
#            pp.pprint(read_tmp3)
        return ParsedGameData, ParsedTalentData
##################################################################################
def get_season_avg(selected_team, ParsedGameData, ParsedTalentData):
#
    s_stats = [0] * 23
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
    for team in ParsedTalentData:
        if (team.get('school') == selected_team):
            s_stats[22] = team.get('talent')
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
    opp_adj_data = [0] * 8
    if (print_get_data == 1):
        print('Selected team = ',selected_team)
    get_data(2,selected_team)
    ParsedGameData, ParsedTalentData= parse_data(2)
    s_stats, opp_list = get_season_avg(selected_team, ParsedGameData, ParsedTalentData)
    opp_stats = numpy.zeros((15,23))
    for x in range(0,s_stats[1]):
        if opp_list[x] != '--':
            selected_team = opp_list[x]
            get_data(2,selected_team)
            ParsedGameData, ParsedTalentData = parse_data(2)
            os_stats, o_opp_list = get_season_avg(selected_team, ParsedGameData, ParsedTalentData)
            opp_stats[x] = os_stats
        else:
            print("They ain't playyyd nobodyyy PAWWWLL")

    oyppa_tot=0
    oypra_tot=0
    otalent_tot = 0
    o_games_tot=0
    for x in range (0,s_stats[1]):
        oyppa_tot = oyppa_tot + opp_stats[x,12]/opp_stats[x,1]
        oypra_tot = oypra_tot + opp_stats[x,8]/opp_stats[x,1]
        otalent_tot = otalent_tot + opp_stats[x,22]
    aoyppa = oyppa_tot / s_stats[1]
    aoypra = oypra_tot / s_stats[1]
    aotalent = otalent_tot / s_stats[1]
#
    tot_att = s_stats[18]+s_stats[20]  # total number of play attempts
    fra_att_r = s_stats[18] / tot_att  # fraction of plays which are rushing
    fra_att_p = s_stats[20] / tot_att  # fraction of plays which are passing
    pts_p_a = (s_stats[2])/((s_stats[8]*fra_att_r+s_stats[12]*fra_att_p)) # points per attempt/yard.
#
    opp_adj_data[1] = aoyppa
    opp_adj_data[2] = aoypra
    opp_adj_data[3] = tot_att
    opp_adj_data[4] = fra_att_r
    opp_adj_data[5] = fra_att_p
    opp_adj_data[6] = pts_p_a
    opp_adj_data[7] = aotalent

    return s_stats, opp_adj_data

##################################################################################
def team_matchup(selected_team1,selected_team2, *args):
# This function calcualtes the matchup between two teams. It takes in the
# season average defenses for pass and rush (%) and weigth's the
# opponent's offense against it.
#
        global adjust_for_talent
        which_option = args[0]
        team_matchup_data = [0] * 17
        if (which_option == 1):
            s_stats1, opp_adj_data1 = get_opp_adj_data(selected_team1)
        else:
            s_stats1 = args[1]
            opp_adj_data1 = args[2]
        s_stats2, opp_adj_data2 = get_opp_adj_data(selected_team2)
#
        aoyppa1 = opp_adj_data1[1]
        aoypra1 = opp_adj_data1[2]
        tot_att1 = opp_adj_data1[3]
        fra_att_r_1 = opp_adj_data1[4]
        fra_att_p_1 = opp_adj_data1[5]
        pts_p_a1 = opp_adj_data1[6]
        if(adjust_for_talent == 1):
            aotalent1 = opp_adj_data1[7]
        else:
            aotalent1 = 1.0

        aoyppa2 = opp_adj_data2[1]
        aoypra2 = opp_adj_data2[2]
        tot_att2 = opp_adj_data2[3]
        fra_att_r_2 = opp_adj_data2[4]
        fra_att_p_2 = opp_adj_data2[5]
        pts_p_a2 = opp_adj_data2[6]
        if(adjust_for_talent == 1):
            aotalent2 = opp_adj_data2[7]
        else:
            aotalent2 = 1.0

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
        pred_pts1 = pred_ypplay1 * pts_p_a1 * min(1,aotalent1/aotalent2)
        pred_pts2 = pred_ypplay2 * pts_p_a2 * min(1,aotalent2/aotalent1)
#
        team_matchup_data[1] = aoyppa1
        team_matchup_data[2] = aoypra1
        team_matchup_data[3] = fra_att_r_1
        team_matchup_data[4] = fra_att_p_1
        team_matchup_data[5] = aoyppa2
        team_matchup_data[6] = aoypra2
        team_matchup_data[7] = fra_att_r_2
        team_matchup_data[8] = fra_att_p_2
        team_matchup_data[9] = pred_yppa1
        team_matchup_data[10] = pred_ypra1
        team_matchup_data[11] = pred_yppa2
        team_matchup_data[12] = pred_ypra2
        team_matchup_data[13] = pred_ypplay1
        team_matchup_data[14] = pred_ypplay2
        team_matchup_data[15] = pred_pts1
        team_matchup_data[16] = pred_pts2


        return s_stats1, s_stats2, opp_adj_data1, opp_adj_data2, team_matchup_data
##################################################################################
def team_season_pred(selected_team1, *args):
        pred_season_data = [0] * 5
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
        if (args[0] ==1):
            s_stats1, opp_adj_data1 = get_opp_adj_data(selected_team1)
        for opponent in FBSList:
            count = count + 1
            if (count == 1):
                if (print_get_data == 1):
                    print('\n')
                    print ('Now Doing:',opponent,'. Team',count,' out of ', len(FBSList))
                if (selected_team1 != opponent):
                    s_stats1, s_stats2, opp_adj_data1, opp_adj_data2, team_matchup_data = team_matchup(selected_team1,opponent, 1)
                    pred_pts1     =     team_matchup_data[15]
                    pred_pts2     =     team_matchup_data[16]
                    pts_for_tot = pred_pts1 + pts_for_tot
                    pts_aga_tot = pred_pts2 + pts_aga_tot
                    if (pred_pts1 > pred_pts2):
                        tot_wins = tot_wins+1
                else:
                    print('Skipping:', opponent)
            else:
                if (print_get_data == 1):
                    print('\n')
                    print ('Now Doing:',opponent,'. Team',count,' out of ',len(FBSList))
                if (selected_team1 != opponent):
                    s_stats1, s_stats2, opp_adj_data1, opp_adj_data2, team_matchup_data = team_matchup(selected_team1,opponent, 2, s_stats1, opp_adj_data1)
                    pred_pts1     =     team_matchup_data[15]
                    pred_pts2     =     team_matchup_data[16]
                    pts_for_tot = pred_pts1 + pts_for_tot
                    pts_aga_tot = pred_pts2 + pts_aga_tot
                    if (pred_pts1 > pred_pts2):
                        tot_wins = tot_wins+1
                else:
                    if (print_get_data == 1):
                        print('Skipping:', opponent)
#
        pred_season_data[0] = tot_wins
        pred_season_data[1] = pts_for_tot
        pred_season_data[2] = pts_aga_tot


        return pred_season_data
##################################################################################
# Set data file
now = datetime.datetime.now()

date = now.strftime("%Y-%m-%d")

DataFile = ('Data_File' + str(date) + '.data')
TalentFile = ('Talent_File' + str(date) + '.data')

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
    print('7: Get Team Rankings')
    print('99: Exit')
    print('##########################','\n')
    option = int(input('Select Option Now:   '))
# Global variables
    print_get_data = 1

    team_done = 'none'
    get_talent = 1
    adjust_for_talent =1

    done_teams = {}

##################################################################################
    if option == 1:
#        get_data(1,'Florida')
#        ParsedGameData=parse_data(1)
        TeamName_opt1 = 'Florida'
        while TeamName_opt1 != '99':
            print('\n','Type "99" to return to main menu','\n')
            TeamName_opt1 = str(input('Enter Team Name:  '))
            if TeamName_opt1 != '99':
                get_data(1,TeamName_opt1)
                ParsedGameData = parse_data(1)
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
        ParsedGameData, ParsedTalentData = parse_data(2)
        WhichWeek=1
        for games in ParsedGameData:
            print('##########################','\n')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(ParsedGameData)
##################################################################################
    if option == 3:

        selected_team = str(input('Enter Team Name:  '))
        get_data(2,selected_team)
        ParsedGameData, ParsedTalentData = parse_data(2)
        s_stats, opp_list = get_season_avg(selected_team,ParsedGameData,ParsedTalentData)
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

        s_stats, opp_adj_data = get_opp_adj_data(selected_team4)
        aoyppa = opp_adj_data[1]
        aoypra = opp_adj_data[2]
        tot_att = opp_adj_data[3]
        fra_att_r = opp_adj_data[4]
        fra_att_p = opp_adj_data[5]
        pts_p_a = opp_adj_data[6]
        aotalent = opp_adj_data[7]

        print('\n')
        print('Passing Allowed % =',round((s_stats[13]*100/s_stats[1])/aoyppa,3))
        print('Rushing Allowed % =',round((s_stats[9]*100/s_stats[1])/aoypra,3))
        print('AVG. Rushing Yards Per Attempt:', round(s_stats[8]/s_stats[1],2), 'AVG. Rushing Yards Per Attempt Allowed:', round(s_stats[9]/s_stats[1],2))
        print('AVG. Passing Yards Per Attempt:', round(s_stats[12]/s_stats[1],2), 'AVG. Passinging Yards Per Attempt Allowed:', round(s_stats[13]/s_stats[1],2))
        print('AVG. Opponent Talent:',round(aotalent,3),'\n')

##################################################################################

    if option == 5:

        print('\n')
        selected_team1 = str(input('Enter Name of Team 1 :  '))
        selected_team2 = str(input('Enter Name of Team 2 :  '))
        adjust_for_talent = int(input('Adjust for Talent Level? 1 = yes, 0 = no  '))

        s_stats1, s_stats2, opp_adj_data1, opp_adj_data2, team_matchup_data = team_matchup(selected_team1,selected_team2,1)
        aoyppa1       =      team_matchup_data[1]
        aoypra1       =      team_matchup_data[2]
        fra_att_r_1   =      team_matchup_data[3]
        fra_att_p_1   =      team_matchup_data[4]
        aoyppa2       =      team_matchup_data[5]
        aoypra2       =      team_matchup_data[6]
        fra_att_r_2   =      team_matchup_data[7]
        fra_att_p_2   =      team_matchup_data[8]
        pred_yppa1    =      team_matchup_data[9]
        pred_ypra1    =     team_matchup_data[10]
        pred_yppa2    =     team_matchup_data[11]
        pred_ypra2    =     team_matchup_data[12]
        pred_ypplay1  =     team_matchup_data[13]
        pred_ypplay2  =     team_matchup_data[14]
        pred_pts1     =     team_matchup_data[15]
        pred_pts2     =     team_matchup_data[16]


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
        tstart = time.time()
        selected_team1 = str(input('Enter Name of the Team  :  '))
        print_get_data = int(input('Print Intermediate Output? 1 = yes, 0 = no  :  '))
        adjust_for_talent = int(input('Adjust for Talent Level? 1 = yes, 0 = no  '))

        pred_season_data = team_season_pred(selected_team1, 1)

        tot_wins = pred_season_data[0]
        pts_for_tot = pred_season_data[1]
        pts_aga_tot = pred_season_data[2]

        print('\n')
        print('##########################')
        print('Total points for:', pts_for_tot)
        print('Total points against:', pts_aga_tot)
        print('Total wins:', tot_wins)
        tend = time.time()
        print('Time elapsed:',round(tend - tstart, 3), 'seconds')


##################################################################################
    if option == 7:
        adjust_for_talent = int(input('Adjust for Talent Level? 1 = yes, 0 = no  '))
        rows = 150
        cols = 4
        rankings = []
        for row in range(rows): rankings += [[None]*cols]
        tstart = time.time()
        print_get_data = 0
#
#       read list of FBS teams from file
        with open('ListOfFBSSchools.csv', 'r') as FBSFile:
            reader = csv.reader(FBSFile)
            FBSList = list(reader)
# Convert to list of strings
        FBSList = list(map(''.join,FBSList))
#
#        rankfile = ('ranking.csv')
#        if os.path.exists(rankfile):
#            print('removing rank file')
#            os.remove(rankfile)
#
        pts_for_tot = 0
        pts_aga_tot = 0
        tot_wins = 0
        count = 0
        index = 0
        print(len(FBSList))
        print(FBSList[1])
        for x in range(2,len(FBSList)):
            team = FBSList[x]
            print('\n')
            print('###############################################################')
            print('Performing Season Calculations for:', team)
            print('###############################################################')
            print('\n')
            count = count + 1
            pred_season_data = team_season_pred(team, count)
            rankings[index][0] = team
            rankings[index][1] = pred_season_data [0]
            rankings[index][2] = pred_season_data [1]
            rankings[index][3] = pred_season_data [2]
            with open('ranking.csv', 'a') as rank_file:
                writer = csv.writer(rank_file)
                writer.writerow(rankings[index])
            index = index + 1
        tend = time.time()
        print('Time elapsed:',round(tend - tstart, 3), 'seconds')
#






##################################################################################

#                pp.pprint(ParsedGameData[games])
##################################################################################
# EXIT
##################################################################################
    if option == 99:
        running = False
        print('\n')
        print('##########################',)
        print('####    Go Gators!!    ###')
        print('##########################',)
        print('\n')
        print('\n')

