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

def fuzzy_search(text_search,type='Name'):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'PS4_games'
    table = dynamodb.Table(table_name)
    response = table.scan()
    records = []
    max_score = 0
    for each in response['Items']:
        each_name = str(each[type])
        #Change score for accuracy
        each_score = fuzz.partial_ratio(text_search.lower(), each_name.lower())

        if each_score>=85:
            # print(each_score)
            # print(each_name)
            if each_score >= max_score:
                records.insert(0, each)
                max_score = each_score
            else:
                records.append(each)
    return records

def image_detect(file_key):

    rekognition = boto3.client("rekognition")
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": 'ps4img',
                "Name": file_key,
            }

        },
        MaxLabels=10,
        MinConfidence=60,

    )
    output_string = ''
    for each in response['Labels']:
        #print(each['Name'],each['Confidence'])
        #output_string.append(each['Name'])
        output_string += ' '+each['Name']
    print(output_string)
    return output_string


def text_detect(file_key):

    rekognition = boto3.client("rekognition")
    response = rekognition.detect_text(
        Image={
            "S3Object": {
                "Bucket": 'ps4img',
                "Name": file_key,
            }

        },
    )
    #print(response)
    output_string = ''
    for each in response['TextDetections']:
        #print(each['Name'],each['Confidence'])
        #output_string.append(each['Name'])
        if each['Confidence']>=95:
            #print(each['DetectedText'])
            output_string += ' '+each['DetectedText']
    print(output_string)
    return output_string



def database_add_label():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'PS4_games'
    table = dynamodb.Table(table_name)
    response = table.scan()

    for each in response['Items']:
        each_name = str(each['Name'])
        labels = image_detect('dynamo/'+each_name+'.jpeg')
        if not labels:
            labels = '/'
        table.update_item(
            Key={
                'Name': each['Name'],
                'FirstChar': each['Name'][0]
            },
            UpdateExpression='SET labels = :val1',
            ExpressionAttributeValues={
                ':val1': labels
            }
        )

    return

def database_add_text():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'PS4_games'
    table = dynamodb.Table(table_name)
    response = table.scan()
    count =0
    for each in response['Items']:
        print(count)
        count +=1
        each_name = str(each['Name'])
        text_str = text_detect('dynamo/'+each_name+'.jpeg')
        if not text_str:
            text_str = '/'
        table.update_item(
            Key={
                'Name': each['Name'],
                'FirstChar': each['Name'][0]
            },
            UpdateExpression='SET text_str = :val1',
            ExpressionAttributeValues={
                ':val1': text_str
            }
        )

    return
def image_text_search(text_search):
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
        if each_score > max_score:
            max_score = each_score
        if each_score>=70:
            print(each_name)
            print(each_score)
            if each_score >= max_score:
                records.insert(0, each)
            else:
                records.append(each)
    print(max_score)
    return records

def search_genre(tmp_key):
    genre_txt = image_detect(tmp_key)
    records = []
    thelist = genre_txt.split()


    if 'Gun' and 'Weapon' in genre_txt:
        records = fuzzy_search('Shooter','Genre')
    elif 'Sports Car' and 'Coupe' in genre_txt:
        records = fuzzy_search('Racing', 'Genre')
    elif 'Military' in genre_txt:
        records = fuzzy_search('Shooter','Genre')
    elif 'Sports' and 'Ball' in genre_txt:
        records = fuzzy_search('Sport', 'Genre')
    elif 'Knight' and 'Samurai' in genre_txt:
        records = fuzzy_search('Adventure', 'Genre')
    if len(records)>10:
        records = records[1:10]

    return records

if __name__ == "__main__":
    # text_search ='callofduty'
    # fuzzy_search(text_search)
    s3_client = boto3.client('s3')
    response = s3_client.upload_file('sample_image1.jpg', 'ps4img', 'tmp/input_tmp.jpg')
    # image_detect('tmp/input_tmp.jpg')
    #database_add_label()
    response = image_detect('tmp/input_tmp.jpg')
    print(response)
    search_genre('tmp/input_tmp.jpg')
    #fuzzy_search(response,'Genre')
    #image_text_search(response)
    #database_add_text()