import requests
from bs4 import BeautifulSoup
import lxml
import re
import app.utils as u
if __name__ == '__main__':
    u.delete_all()
    url = 'https://psdeals.net/ca-store/collection/new_games?platforms=ps4'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "lxml")
    games = soup.find_all('a',{'class':'game-collection-item-link'})
    for game in games:
        url = game.attrs.get('href')
        url = 'https://psdeals.net/'+url
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        date = soup.find('span',{'itemprop':'releaseDate'}).get_text()
        name = game.find('p',{'class':'game-collection-item-details-title'})
        img = game.find('img',{'itemprop':'image'})
        price = game.find('span',{'class':'game-collection-item-regular-price'})
        name = name.get_text()
        img = img.attrs.get('data-src')
        price = price.get_text()[1:]
        u.update_new_game(name, img, price,date)
