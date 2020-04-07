import boto3
from boto3.dynamodb.conditions import Key, Attr

#Put a new item to the table
def put_item (game_name,genre,wiki_link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')
    first_char = game_name[0]
    print(first_char)
    table.put_item(
        Item={
            'FirstChar': first_char,
            'Name': game_name,
            'Genre': genre,
            'Wiki': wiki_link,
            "Amazon_price":'/',
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
    No = 1
    for i in response['Items']:
        i['No']= No
        No += 1
        records.append(i)
    return records

def update_new_game (game_name,img,price,date):
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
        }
    )
    return

def list_all_new_games():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('New_game')

    response = table.scan()

    records = []
    No = 1
    for i in response['Items']:
        i['No']= No
        No += 1
        records.append(i)
    return records

def delete_all():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')

    response = table.scan()
    for each in response['Items']:
        first_char = each['Name'][0]
        response = table.delete_item(
            Key = {
                'Name':each['Name'],
                'FirstChar':first_char
            }

        )

def search_name(text_search):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')

    response = table.scan(
        FilterExpression= Attr("Genre").contains(text_search))
    for i in response['Items']:
        print(i)

    return



if __name__ == "__main__":
    delete_all()