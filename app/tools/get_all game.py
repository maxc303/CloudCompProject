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
    for i in range(1,80):
        url = prefix+str(i)+suffix
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        games = soup.find_all('a',{'class':'game-collection-item-link'})
        for game in games:
            url = game.attrs.get('href')
            url = 'https://psdeals.net/'+url
            result = requests.get(url)
            soup = BeautifulSoup(result.content, "lxml")
            date = soup.find('span',{'itemprop':'releaseDate'}).get_text()
            div = soup.find('div',{'class':'game-info'})
            p = div.find_all('p')
            if(str(p[1]).find('href')==-1):
                genre = '/'
            else:
                genre = p[1].find('a').get_text()
            link = soup.find('a',{'class':'game-buy-button-href'}).attrs.get('href')
            img = game.find('img', {'itemprop': 'image'})
            img = img.attrs.get('data-src')
            img = ''.join(img.split('&')[:-2])
            name = game.find('p',{'class':'game-collection-item-details-title'})
            price = game.find('span',{'class':'game-collection-item-regular-price'})
            name = name.get_text()
            price = price.get_text()[1:]
            print(name,price,date,genre)
            print(img)
            u.put_item(name,genre,img,price,date,link)
            time.sleep(0.1)
