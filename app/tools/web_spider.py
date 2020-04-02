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
                url = str(url).split("'")[1]
                name = re.findall(r'">(.+?)</a>', str(td[0]))
                if(str(name).__contains__('"')):
                    name = str(name).split('"')[1]
                else:
                    name = str(name).split("'")[1]
                if(td[1].find('li')):
                    li = td[1].find('li')
                    genre = re.findall(r'<li>(.+?)</li>', str(li))
                    if(str(genre).__contains__('"')):
                        genre = str(genre).split('"')[1]
                    else:
                        genre = str(genre).split("'")[1]
                    genre = genre.split("\\n")[0]
                else:
                    genre = re.findall(r'<td>(.+?)</td>', str(td[1]), re.S)
                    if (str(genre).__contains__('"')):
                        genre = str(genre).split('"')[1]
                    else:
                        genre = str(genre).split("'")[1]
                    genre = genre.split("\\n")[0]
                    genre = genre.split("\\n")[0]
                print("url",str(url))
                print("name",str(name))
                print('genre',genre)
                if(name!=''):
                    u.put_item(str(name), str(genre),str(url))


