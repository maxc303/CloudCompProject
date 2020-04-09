import requests
from bs4 import BeautifulSoup
import lxml
import re
import app.utils as u
if __name__ == '__main__':
    name = 'Asdivine Hearts'
    name = '+'.join(name.split(' '))
    url = 'https://store.playstation.com/en-ca/product/UP3984-CUSA11630_00-APP0000000000000'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "lxml")
    print(soup)