import requests
from bs4 import BeautifulSoup
import lxml
import boto3
import json
def update_new_game (game_name,img,price,date,link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('New_game')
    first_char = game_name[0]
    print(first_char)
    table.put_item(
        Item={
            'FirstChar': first_char,
            'Name': game_name,
            'img': img,
            'price': price,
            'date': date,
            'ps_link':link,
        }
    )
    return

def update_free_game (game_name,img,price,date,link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Free_games')
    first_char = game_name[0]
    print(first_char)
    table.put_item(
        Item={
            'FirstChar': first_char,
            'Name': game_name,
            'img': img,
            'price': price,
            'date': date,
            'ps_link':link,
        }
    )
    return


def delete_all_free():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Free_games')

    response = table.scan()
    for each in response['Items']:
        first_char = each['Name'][0]
        response = table.delete_item(
            Key = {
                'Name':each['Name'],
                'FirstChar':first_char
            }

        )

def delete_all_new():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('New_game')

    response = table.scan()
    for each in response['Items']:
        first_char = each['Name'][0]
        response = table.delete_item(
            Key = {
                'Name':each['Name'],
                'FirstChar':first_char
            }

        )

def update_will_release_game (game_name,img,price,date,link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Will_release_games')
    first_char = game_name[0]
    print(first_char)
    table.put_item(
        Item={
            'FirstChar': first_char,
            'Name': game_name,
            'img': img,
            'price': price,
            'date': date,
            'ps_link':link,
        }
    )
    return

def delete_all_will():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Will_release_games')

    response = table.scan()
    for each in response['Items']:
        first_char = each['Name'][0]
        response = table.delete_item(
            Key = {
                'Name':each['Name'],
                'FirstChar':first_char
            }

        )

#main function of the background process

def lambda_handler(event, context):
    delete_all_new()
    url = 'https://psdeals.net/ca-store/collection/new_games?platforms=ps4'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")
    games = soup.find_all('a',{'class':'game-collection-item-link'})
    i = 1
    for game in games:
        url = game.attrs.get('href')
        url = 'https://psdeals.net/'+url
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "html.parser")
        date = soup.find('span',{'itemprop':'releaseDate'}).get_text()
        link = soup.find('a', {'class': 'game-buy-button-href'}).attrs.get('href')
        name = game.find('p',{'class':'game-collection-item-details-title'})
        img = game.find('img',{'itemprop':'image'})
        price = game.find('span',{'class':'game-collection-item-regular-price'})
        name = name.get_text()
        img = img.attrs.get('data-src')
        img = ''.join(img.split('&')[:-2])
        price = price.get_text()[1:]
        print(name,'    ',price)
        update_new_game(name, img, price,date,link)
        i+=1
        if(i>20):
            break
    print('new games uploaded')
#get free games
    delete_all_free()
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
        update_free_game(name, img, price, date, link)
        i += 1
        if (i > 20):
            break
    print('free games uploaded')
    #upcoming games
    delete_all_will()
    url = 'https://psdeals.net/ca-store/collection/will_be_released?platforms=ps4'
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
        update_will_release_game(name, img, price, date, link)
        i += 1
        if (i > 20):
            break
    print('upcoming games uploaded')

# TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('background function completed')
    }

