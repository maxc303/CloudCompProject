import requests
from bs4 import BeautifulSoup
import lxml
import re
import app.utils as u
if __name__ == '__main__':
    prefix = "https://www.pricecharting.com/search-products?q="
    suffix = "&type=videogames&sort=name&console-uid=G53&region-name=ntsc&exclude-variants=false"
    records = u.list_all()
    i=0
    for record in records:
        i+=1
        if(i<429):
            continue
        name = record['Name']
        name = '+'.join(name.split(' '))
        url = prefix + name + suffix
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        result = soup.find_all('table',{'id':'games_table'})
        if(len(result)==0):
            result = soup.find_all('tr',{'data-source-name':"Amazon"})
            if(len(result)==0):
                u.update_price(record['Name'], '/', '/')
                continue
            tmp = str(result[2])
            tmp = tmp.replace('\n', '')
            if (tmp.find('span') == -1):
                amazon_price = '/'
            else:
                result = result[2].find_all('span', 'js-price')
                amazon_price = result[0].get_text().split('$')[1]

            result = soup.find_all('tr', {'data-source-name': "eBay"})
            tmp=str(result[2])
            tmp = tmp.replace('\n','')
            if(tmp.find('span')==-1):
                eBay_price = '/'
            else:
                result = result[2].find_all('span', 'js-price')
                eBay_price = result[0].get_text().split('$')[1]
        else:
            a=result[0].find('a')
            url = re.findall(r'href="(.+?)"', str(a))[0]
            result = requests.get(url)
            soup = BeautifulSoup(result.content, "lxml")
            if (soup.find_all('table', {'id': 'games_table'})):
                result = soup.find_all('span', {'class': 'js-price'})
                if (result[2].get_text() == ''):
                    Amazon_price = '/'
                else:
                    Amazon_price = result[2].get_text().split('$')[1]
                if (result[0].get_text() == ''):
                    eBay_price = '/'
                else:
                    eBay_price = result[0].get_text().split('$')[1]
                u.update_price(record['Name'], amazon_price, eBay_price)
                print('amazon price', amazon_price, ', ebay price', eBay_price, '  ', record['Name'], ' updated')
                continue
            result = soup.find_all('tr', {'data-source-name': "Amazon"})
            tmp = str(result[2])
            tmp = tmp.replace('\n', '')
            if (tmp.find('span') == -1):
                amazon_price = '/'
            else:
                result = result[2].find_all('span', 'js-price')
                amazon_price = result[0].get_text().split('$')[1]

            result = soup.find_all('tr', {'data-source-name': "eBay"})
            tmp = str(result[2])
            tmp = tmp.replace('\n', '')
            if (tmp.find('span') == -1):
                eBay_price = '/'
            else:
                result = result[2].find_all('span', 'js-price')
                eBay_price = result[0].get_text().split('$')[1]
        u.update_price(record['Name'],amazon_price,eBay_price)
        print('amazon price',amazon_price,', ebay price',eBay_price,'  ',record['Name'],' updated')