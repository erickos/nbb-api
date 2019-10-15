from bs4 import BeautifulSoup
import requests

url = 'https://lnb.com.br/nbb/estatisticas/pontos/?aggr=sum&type=athletes&suffered_rule=0&season%5B%5D=47&phase%5B%5D=1&round%5B%5D=1'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

print(soup.find_all('tr'))