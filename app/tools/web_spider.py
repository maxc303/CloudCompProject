import requests
import re
import app.utils as u
from bs4 import BeautifulSoup
if __name__ == '__main__':
    file = open('ps4_games.html','r',encoding='utf-8')
    soup = BeautifulSoup(file, 'html.parser')
    text = soup.find_all('tr',)
    for tr in text:

        print('-'*100)
        td = tr.find_all('td')
        if(td[0].find('a')):
            if not(td[1].find('a')):
                url = re.findall(r'href="(.+?)"', str(td[0]))
                name = re.findall(r'">(.+?)</a>', str(td[0]))
                date = re.findall(r'">(.+?)</span>', str(td[6]))
                if(td[1].find('li')):
                    li = td[1].find('li')
                    genre = re.findall(r'<li>(.+?)</li>', str(li))
                else:
                    genre = re.findall(r'<td>(.+?)</td>', str(td[1]), re.S)
                print("url",str(url))
                print("name",str(name))
                print('genre',genre)
                print('date',date)
                u.put_item(str(name), str(genre),str(url))


