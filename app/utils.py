import boto3
from boto3.dynamodb.conditions import Key, Attr
from fuzzysearch import find_near_matches
from fuzzywuzzy import fuzz
#Put a new item to the table
def put_item (game_name,genre,img,price,date,link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')
    first_char = game_name[0]
    print(first_char)
    table.put_item(
        Item={
            'FirstChar': first_char,
            'Name': game_name,
            'Genre': genre,
            'img': img,
            "price":price,
            'date' :date,
            'ps_link': link,
        }
    )
    return

def update_price(game_name,amazon_price,eBay_price):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')
    first_char = game_name[0]
    table.update_item(

        Key = {
              'FirstChar': first_char,
              'Name': game_name
          },
    UpdateExpression = 'SET Amazon_price= :val1, eBay_price= :val2',
    ExpressionAttributeValues = {
        ':val1': amazon_price,
        ':val2': eBay_price
    }
    )

def list_all():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')

    response = table.scan()

    records = []

    for i in response['Items']:
        records.append(i)
    return records

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

def update_will_free_game (game_name,img,price,date,link):
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


def list_all_new_games():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('New_game')

    response = table.scan()

    records = []
    for i in response['Items']:
        records.append(i)
    records.sort(key=lambda k: (k.get('date', 0)),reverse=True)
    return records

def list_all_free_games():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Free_games')

    response = table.scan()

    records = []
    for i in response['Items']:
        records.append(i)
    return records

def list_all_will_release_games():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Will_release_games')

    response = table.scan()

    records = []
    for i in response['Items']:
        records.append(i)
    records.sort(key=lambda k: (k.get('date', 0)), reverse=False)
    return records

def list_search_results(search_txt):
    table_name ='PS4_games'

    response = search_name(search_txt,table_name)

    records = []
    No = 1
    for i in response['Items']:
        i['No']= No
        No += 1
        records.append(i)
    return records

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

def search_name(text_search,table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression= Attr("Name").contains(text_search))
    for i in response['Items']:
        print(i)

    return response

def fuzzy_search(text_search):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'PS4_games'
    table = dynamodb.Table(table_name)
    response = table.scan()
    records = []
    max_score = 0
    for each in response['Items']:
        each_name = str(each['Name'])
        #Change score for accuracy
        each_score = fuzz.partial_ratio(text_search.lower(), each_name.lower())

        if each_score>=85:
            print(each_score)
            if each_score >= max_score:
                records.insert(0, each)
                max_score = each_score
            else:
                records.append(each)

    return records


if __name__ == "__main__":
    text_search ='callofduty'
    fuzzy_search(text_search)
