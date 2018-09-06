import requests
from bs4 import BeautifulSoup
import re


def get_stats(N, date):
    '''
    Get the Statistics from the N top players from ATP
    at a certain date.
    Returns a list of dictionaries with the Statistics
    '''

    page_ranking = requests.get('https://www.atpworldtour.com/en/rankings/singles?rankDate=' \
                                + date + '&rankRange=1-' \
                                + str(N))
    ranking = BeautifulSoup(page_ranking.content, 'html.parser')
    ranking_list = list(ranking.findAll('td', {'class':'player-cell'}))
    rank_url = []

    for i in range(0, N):

        a = str(list(ranking_list[i])[1])
        b = 'https://www.atpworldtour.com' + \
            a[(a.find('href="')+6):(a.find('>')-1)].replace('overview','')
        rank_url.append([i+1,b])

    players = []
    player_dict = {}

    for i in range(0,N):

        player_dict = {}

        print('Rank in Evaluation: ', i+1, end = '\r')

        page_plrstats = requests.get(rank_url[i][1] + 'player-stats')
        plrstats = BeautifulSoup(page_plrstats.content, 'html.parser')

        player_dict['rank'] = i+1

        # Name
        try:
            a = plrstats.findAll('h1', {'class':'page-title'})
            b = str(a).replace(' ','')
            c = b[(b.find('\n')+1):(b.find('\r\n</h1>'))]
    #         c = re.sub(r"(\w)([A-Z])", r"\1 \2", c)
            player_dict['name'] = c
        except:
            print('name',i+1)

        # Nationality
        try:
            a = plrstats.findAll('div', {'class':'player-flag-code'})
            b = str(a)
            c = b[(b.find('>')+1):b.find('</')]
            player_dict['nat'] = c
        except:
            print('nat',i+1)

        # Age
        try:
            a = plrstats.findAll('div', {'class':'table-big-value'})
            b = list(list(a)[0])[0]
            c = int(b[(b.find('\n')+1):b.find(' ')])
            player_dict['age'] = c
        except:
            print('age',i+1)

        # Birth
        try:
            a = plrstats.findAll('div', {'class':'table-big-value'})
            b = str(list(list(a)[0])[1]).replace(' ','')
            c = b[(b.find('(')+1):(b.find(')'))]
            player_dict['birth'] = c
        except:
            print('birth',i+1)

        # Turned Pro
        try:
            a = plrstats.findAll('div', {'class':'table-big-value'})
            b = str(list(a)[1]).replace(' ','')
            c = int(b[(b.find('\n')+1):(b.find('</div>'))])
            player_dict['turned_pro'] = c
        except:
            print('turned pro',i+1)

        # Weight (kg)
        try:
            a = plrstats.findAll('span', {'class':'table-weight-kg-wrapper'})
            b = str(a)
            c = int(b[(b.find('(')+1):b.find('kg)')])
            player_dict['weight'] = c
        except:
            print('weight',i+1)

        # Height (cm)
        try:
            a = plrstats.findAll('span', {'class':'table-height-cm-wrapper'})
            b = str(a)
            c = int(b[(b.find('(')+1):b.find('cm)')])
            player_dict['height'] = c
        except:
            print('height',i+1)

        # Plays
        try:
            a = plrstats.findAll('div', {'class':'table-value'})
            b = str(list(a)[2]).replace(' ','')
            c = b[(b.find('\n')+1):b.find('Backhand')]
            if c != "</div":
                player_dict['plays'] = c
        except:
            print('plays',i+1)

        # Aces
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[0])[3])[1])
            c = int(b[37:(b.find(r'<\r\n\t\t</td>\n</tr>')-14)].replace(',',''))
            player_dict['aces'] = c
        except:
            print('aces',i+1)

        # Double-Faults
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[3])
            c = int(b[46:-15].replace(',',''))
            player_dict['double_faults'] = c
        except:
            print('double faults',i+1)

        # 1st Serve (%)
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[5])
            c = int(b[42:-16])
            player_dict['f_serve'] = c
        except:
            print(r'1st Serve (%)',i+1)

        # 1st Serve Won (%)
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[7])
            c = int(b[53:-16])
            player_dict['f_serve_won'] = c
        except:
            print(r'1st Serve Won (%)',i+1)

        # 2nd Serve Won (%)
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[9])
            c = int(b[53:-16])
            player_dict['s_serve_won'] = c
        except:
            print(r'2nd Serve Won (%)',i+1)

        # Break Points Faced
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[11])
            c = int(b[51:-15].replace(',',''))
            player_dict['break_faced'] = c
        except:
            print('break faced',i+1)

        # Break Points Saved (%)
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[13])
            c = int(b[51:-16].replace(',',''))
            player_dict['break_saved'] = c
        except:
            print(r'break saved (%)',i+1)

        # Service Games Played
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[15])
            c = int(b[53:-15].replace(',',''))
            player_dict['serve_played'] = c
        except:
            print('serve played',i+1)

        # Service Games Won
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[17])
            c = int(b[50:-16])
            player_dict['serve_won'] = c
        except:
            print('serve won',i+1)

        # Service Points Won
        try:
            a = plrstats.find('table', {'class':'mega-table'})
            b = str(list(list(a)[3])[19])
            c = int(b[57:-16])
            player_dict['serve_points_won'] = c
        except:
            print('service points won',i+1)

        # First Serve Return Points Won (%)
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[1])
            c = int(b[60:-16])
            player_dict['re_f_serve_won'] = c
        except:
            print('return f serve won',i+1)

        # Second Serve Return Points Won (%)
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[3])
            c = int(b[60:-16])
            player_dict['re_s_serve_won'] = c
        except:
            print('return s serve won',i+1)

        # Break Point Opportunities
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[5])
            c = int(b[59:-15].replace(',',''))
            player_dict['break_opp'] = c
        except:
            print('break opportunities',i+1)

        # Break Points Converted (%)
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[7])
            c = int(b[55:-16])
            player_dict['break_conv'] = c
        except:
            print(r'break converted (%)',i+1)

        # Return Games Played
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[9])
            c = int(b[52:-15].replace(',',''))
            player_dict['re_games_played'] = c
        except:
            print('return games played',i+1)

        # Return Games Won (%)
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[11])
            c = int(b[49:-16])
            player_dict['re_games_won'] = c
        except:
            print(r'return games won (%)',i+1)

        # Return Points Won (%)
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[13])
            c = int(b[49:-16])
            player_dict['re_points_won'] = c
        except:
            print(r'return points won (%)',i+1)

        # Total Points Won (%)
        try:
            a = plrstats.findAll('table', {'class':'mega-table'})
            b = str(list(list(list(a)[1])[3])[15])
            c = int(b[49:-16])
            player_dict['total_points_won'] = c
        except:
            print(r'total points won (%)',i+1)

        page_plrstats = requests.get(rank_url[i][1] + 'overview')
        plrstats = BeautifulSoup(page_plrstats.content, 'html.parser')

        # Prize Career
        try:
            a = plrstats.findAll('div', {'class':'stat-value'})
            b = str(list(a)[-1])
            c = int(b[(b.find('singles="$')+10):b.find('">')].replace(',',''))
            player_dict['prize'] = c
        except:
            print('prize career',i+1)

        # Prize Year
        try:
            a = plrstats.findAll('div', {'class':'stat-value'})
            b = str(list(a)[-5])
            c = int(b[(b.find('data-singles')+15):(b.find('">'))].replace(',',''))
            player_dict['prize_year'] = c
        except:
            print('prize year',i+1)

        # Score
        try:
            a = plrstats.findAll('div', {'class':'stat-value'})
            b = str(list(a)[-3])
            c = b[(b.find('data-singles')+14):(b.find('">'))].replace(',','')
            player_dict['score'] = c
        except:
            print('score',i+1)

        # Score Year
        try:
            a = plrstats.findAll('div', {'class':'stat-value'})
            b = str(list(a)[-7])
            c = b[(b.find('data-singles')+14):(b.find('">'))].replace(',','')
            player_dict['score_year'] = c
        except:
            print('score year',i+1)

        # Coaches
        try:
            a = plrstats.findAll('div', {'class':'table-value'})
            b = str(list(a)[-1]).replace(' ','')
            c = b[26:-8]
            player_dict['coach'] = c
        except:
            print('coach',i+1)

        # Birthplace
        try:
            a = plrstats.findAll('div', {'class':'table-value'})
            b = str(list(a)[0]).replace(' ','')
            c = b[26:-8]
            player_dict['place_birth'] = c
        except:
            print('place birth',i+1)

        # Residence
        try:
            a = plrstats.findAll('div', {'class':'table-value'})
            b = str(list(a)[1]).replace(' ','')
            c = b[24:-6]
            player_dict['residence'] = c
        except:
            print('residence',i+1)

        players.append(player_dict)

    return players
