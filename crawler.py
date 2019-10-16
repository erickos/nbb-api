from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import json
app = Flask(__name__)

seasons = ['1', '2', '3', '4', '8', '15', '20', '27', '34', '41', '47', '54']

@app.route('/points')
def points():
    player = request.args.get('player')
    week = int(request.args['week'])
    season = int(request.args['season'])

    url = ''

    if player:
        pass
    else:
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

#@app.route('/athletes')