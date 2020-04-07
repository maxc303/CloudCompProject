import requests
from bs4 import BeautifulSoup
import lxml
import re
import app.utils as u
import time
if __name__ == '__main__':
    # u.delete_all()
    prefix = 'https://psdeals.net/ca-store/all-games/'
    suffix = '?sort=rating-desc&platforms=ps4'
    for i in range(1,25):
        url = prefix+str(i)+suffix
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        games = soup.find_all('a',{'class':'game-collection-item-link'})
        for game in games:
            url = game.attrs.get('href')
            url = 'https://psdeals.net/'+url
            result = requests.get(url)
            soup = BeautifulSoup(result.content, "lxml")
            if(soup.find('span',{'itemprop':'releaseDate'})==None):
                date = '/'
            else:
                date = soup.find('span',{'itemprop':'releaseDate'}).get_text()

            img = game.find('img', {'itemprop': 'image'})
            img = img.attrs.get('data-src')
            img = ''.join(img.split('&')[:-2])
            name = game.find('p',{'class':'game-collection-item-details-title'})
            price = game.find('span',{'class':'game-collection-item-regular-price'})
            name = name.get_text()
            price = price.get_text()[1:]
            # u.update_new_game(name, img, price,date)
            print(name,price,date)
            print(img)
            time.sleep(0.1)
