# -*- coding: utf-8 -*-

from datetime import datetime
import requests
import lxml.html


class TargetSelect:
    def __init__(self, name=None, select_term=None):
        self.name = name
        self.select_term = select_term

title = TargetSelect('product_title', 'h1#title > span#productTitle')
td = TargetSelect('area', 'tr#places_area__row > td.w2p_fw')
size = TargetSelect('memory', 'div#variation_size_name > div.a-row > span.selection')
color = TargetSelect('color', 'div#variation_color_name > div.a-row > span.selection')
soldby = TargetSelect('soldby', 'div#shipsFromSoldBy_feature_div > div#merchant-info')
price = TargetSelect('price', 'tr#priceblock_ourprice_row > td.a-span12 > span#priceblock_ourprice')
timestamp = TargetSelect('timestamp', '{:%Y%m%d%H%M%S}')

def scrape(html):
    targets = [title, size, color, soldby, price ]
    results = {}
    for ele in targets:
        results[ele.name] = None
    tree = lxml.html.fromstring(html)
    for ele in targets:
        select_res = tree.cssselect(ele.select_term )
        if select_res:
            results[ele.name] = " ".join(select_res[0].text_content().split() )
        else:
            results[ele.name] = '*** failed ***'
        print(ele.name + ': ' + results[ele.name])
    results[timestamp.name] = timestamp.select_term.format(datetime.now() )
    return results

if __name__ == '__main__':
    seed_url = 'https://www.amazon.com/dp/B01J8PBEUM?th=1'
    response = requests.get(seed_url)
    html = response.text
    # html = '<a></a>'
    results = scrape(html)
    print(timestamp.name + ': ' + results[timestamp.name] )