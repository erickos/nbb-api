import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
app = Flask(__name__)

seasons = ['1', '2', '3', '4', '8', '15', '20', '27', '34', '41', '47', '54']

all_players_json = None

def create_dict_link_to_name():
    # criando as listas de cada time
    _teams_name_page_url = 'https://lnb.com.br/nbb/equipes'
    _teams_name_page = requests.get( _teams_name_page_url )
    _teams_name_soup = BeautifulSoup( _teams_name_page.content, 'html.parser' )

    _teams_name_links = _teams_name_soup.find_all('div', class_="large-12 small-12 medium-12 columns")[1].find_all('a')

    _dict_link_to_name = {}

    for link in _teams_name_links:
        _page = requests.get(link['href'])
        _soup = BeautifulSoup( _page.content, 'html.parser' )

        _team_name = _soup.find('strong', class_='whitet title').text

        _dict_link_to_name[ link['href'] ] = _team_name

    return _dict_link_to_name

@app.route('/', methods=['GET'])
def index():
    return 'BEM VINDO !!!' 

@app.route('/points', methods=['GET'])
def points():
    player = request.args.get('player')
    week = int(request.args['week'])
    season = int(request.args['season'])

    url = '' 
    url = 'https://lnb.com.br/nbb/estatisticas/pontos/?aggr=sum&type=athletes&suffered_rule=0&season[]='+seasons[season-1]+'&phase[]=1&round[]='+str(week)+'&wherePlaying=-1'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    rows = soup.find('tbody').find_all('tr')
    players_stats_points = { 'players': [] }
    
    players = []

    for row in rows:
        cols = row.find_all('td')
        player_in_row = {
            'name': cols[1].find('a').get_text(),
            'team': cols[2].find('a').get_text(),
            'games_played': int(cols[3].text.strip()),
            'minutes_played': int(cols[4].text.strip()),
            'points': int(cols[5].text.strip()),
            'three_pts_basket': int(cols[6].text.strip()), 
            'two_pts_basket': int(cols[7].text.strip()),
            'free_throw_pts': int(cols[8].text.strip()) 
        }
        players.append(player_in_row)

    players_stats_points['players'] = players

    return players_stats_points

@app.route('/rebounds', methods=['GET'])
def rebounds():
    week = int(request.args['week'])
    season = int(request.args['season'])

    url = 'https://lnb.com.br/nbb/estatisticas/rebotes/?aggr=sum&type=athletes&suffered_rule=0&season[]='+seasons[season-1]+'&phase[]=1&round[]='+str(week)+'&wherePlaying=-1'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    rows = soup.find('tbody').find_all('tr')
    players_stats_rebounds = { 'players': [] }
    
    players = []

    for row in rows:
        cols = row.find_all('td')
        player_in_row = {
            'name': cols[1].find('a').get_text(),
            'team': cols[2].find('a').get_text(),
            'games_played': int(cols[3].text.strip()),
            'minutes_played': int(cols[4].text.strip()),
            'rebounds': int(cols[5].text.strip()),
            'off_rebounds': int(cols[6].text.strip()), 
            'def_rebounds': int(cols[7].text.strip()),
        }
        players.append(player_in_row)

    players_stats_rebounds['players'] = players

    return players_stats_rebounds

@app.route('/assists', methods=['GET'])
def assists():
    week = int(request.args['week'])
    season = int(request.args['season'])

    url = 'https://lnb.com.br/nbb/estatisticas/assistencias/?aggr=sum&type=athletes&suffered_rule=0&season[]='+seasons[season-1]+'&phase[]=1&round[]='+str(week)+'&wherePlaying=-1'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    rows = soup.find('tbody').find_all('tr')
    players_stats_assists = { 'players': [] }
    
    players = []

    for row in rows:
        cols = row.find_all('td')
        player_in_row = {
            'name': cols[1].find('a').get_text(),
            'team': cols[2].find('a').get_text(),
            'games_played': int(cols[3].text.strip()),
            'minutes_played': int(cols[4].text.strip()),
            'assists': int(cols[5].text.strip()),
            'assists_err': int(cols[6].text.strip()), 
            'assists_per_err': int(cols[7].text.strip()),
        }
        players.append(player_in_row)

    players_stats_assists['players'] = players

    return players_stats_assists

def get_athletes():
    initial_url = 'https://lnb.com.br/nbb/atletas/'
    page = requests.get(initial_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    teams_link_list = soup.find('div', {"class": "column players_archive_select_team"}).find_all('li')

    final_dict = { 'team_to_players': [] }
    players_by_team = {}
    link_to_team_name = {}  

    # Dicionario para guardar referencia entre o link de acesso e o nome do time
    link_to_team_name = create_dict_link_to_name()

    # criando as listas de cada time
    teams_name_page_url = 'https://lnb.com.br/nbb/equipes'
    teams_name_page = requests.get(teams_name_page_url)
    teams_name_soup = BeautifulSoup(teams_name_page.content, 'html.parser')

    teams_name_list = teams_name_soup.find_all('div', class_="name_team_archive")

    for current_team in teams_name_list:
        team_name = current_team.find('strong').text.upper()
        players_by_team[team_name] = []  
    #####                     #####

    for team in teams_link_list:
        team_url = team.find('a')['href'] 

        team_page = requests.get( team_url )
        team_soup = BeautifulSoup(team_page.content, 'html.parser')
        team_players_resultset = team_soup.find('section', class_='players_archive_screen_one').find('div', class_='large-12 small-12 medium-12 columns').findChildren('a', recursive=False)

        for player in team_players_resultset:
            curr_player_info = {}
            curr_player_info['player_page_link'] = player['href']

            player_page = requests.get( player['href'] )
            player_soup = BeautifulSoup( player_page.content, 'html.parser')
            

            try:
                player_general_info = player_soup.find('table', class_='ficha_tecnica_athlete_stats show-for-small-only').find_all('tr')

                # player name 
                curr_player_info['fullname'] = player_general_info[0].find_all('td')[1].text
                # player position
                curr_player_info['position'] = player_general_info[1].find_all('td')[1].text
                # player birth date
                curr_player_info['date'] = player_general_info[2].find_all('td')[1].text
                
                # tratamento altura e peso
                aux_alt_peso = player_general_info[3].find_all('td')[1].text.split('/')
                curr_player_info['height'] = float(aux_alt_peso[0].strip())
                curr_player_info['weight'] = float(aux_alt_peso[1].strip().replace('kg',''))

                curr_player_info['birth_place'] = player_general_info[4].find_all('td')[1].text

                # tratando caso apareça mais de um time, ocorre quando o jogador participou do Jogos das Estrelas
                curr_player_team_info = player_general_info[5].find_all('a')

                if( len(curr_player_team_info) == 1 ):
                    curr_player_info['team_page_link'] = curr_player_team_info[0]['href']
                    curr_player_info['team_name'] = link_to_team_name[ curr_player_team_info[0]['href'] ].upper()
                else:
                    curr_player_info['team_page_link'] = curr_player_team_info[1]['href']
                    curr_player_info['team_name'] =link_to_team_name[ curr_player_team_info[1]['href'] ].upper()

                # Link para o avatar do atleta
                curr_player_info['photo_src_link'] = player_soup.find( 'div', class_='photo_athlete_blue large-2 medium-6 small-12 columns' ).find('img')['src']

                # Nome identificador do atleta '# (shirt number) name'
                curr_player_info['name'] = player_soup.find( 'div', class_='large-9 medium-12 small-12 columns athlete_stats' ).find('h1').text.replace('/','').replace('<strong>','').strip() 

                # Numero aparicoes no Jogo das estrelas
                curr_player_info['allstar_appearances'] = player_soup.find('table', class_='ficha_tecnica_athlete_stats hide-for-small-only').find_all('tr')[3].find_all('td')[1].text

                # adicionando a lista de jogadores daquele time
                players_by_team[ curr_player_info['team_name'] ].append( curr_player_info )
            except:
                print( 'Current Player : ', player['href'], ' from : ', team_url )

    final_dict['team_to_players'].append( players_by_team )

    return final_dict

@app.route('/athletes', methods=['GET'])
def athletes():
    if( not all_players_json ):
        all_players_json = get_athletes()

    return all_players_json

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)