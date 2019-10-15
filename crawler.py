from flask import Flask, request
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

seasons = ['1', '2', '3', '4', '8', '15', '20', '27', '34', '41', '47', '54']

def get

@app.route('/points')
def points():
    player = request.args.get('player')
    week = request.args['week']
    season = request.args['season']

    url = ''

    if player:
        pass
    else:
        url = 'https://lnb.com.br/nbb/estatisticas/pontos/?aggr=sum&type=athletes&suffered_rule=0&season[]='+seasons[season-1]+'&phase[]=1&round[]='+week+'&wherePlaying=-1'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

    return str(soup.find('tbody'))

#@app.route('/athletes')