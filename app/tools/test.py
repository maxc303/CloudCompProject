import requests
from bs4 import BeautifulSoup
import boto3
import json
import app.utils as u

if __name__ == '__main__':
    u.delete_all_free()
    url = 'https://psdeals.net/ca-store/collection/free_ps_plus?platforms=ps4'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")
    games = soup.find_all('a', {'class': 'game-collection-item-link'})
    i = 1
    for game in games:
        url = game.attrs.get('href')
        url = 'https://psdeals.net/' + url
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "html.parser")
        date = soup.find('span', {'itemprop': 'releaseDate'}).get_text()
        link = soup.find('a', {'class': 'game-buy-button-href'}).attrs.get('href')
        name = game.find('p', {'class': 'game-collection-item-details-title'})
        img = game.find('img', {'itemprop': 'image'})
        price = game.find('span', {'class': 'game-collection-item-regular-price'})
        name = name.get_text()
        img = img.attrs.get('data-src')
        img = ''.join(img.split('&')[:-2])
        price = price.get_text()[1:]
        print(name, '    ', price)
        u.update_will_free_game(name, img, price, date, link)
        i += 1
        if (i > 20):
            break