import requests
import json
if __name__ == '__main__':
    target = 'https://en.wikipedia.org/wiki/List_of_PlayStation_4_games#0%E2%80%939'
    req = requests.get(url=target)
    file = '../spider.json'

    fo = open("test.txt", "w")
    print
    "文件名为: ", fo.name
    str = "菜鸟教程"
    fo.write(str)

    # 关闭文件
    fo.close()