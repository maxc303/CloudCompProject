import boto3
from boto3.dynamodb.conditions import Key, Attr
from fuzzysearch import find_near_matches
from fuzzywuzzy import fuzz


def put_item (game_name,genre,img,price,date,link):
    '''
    add data into dynamodb
    '''
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


def list_all():
    '''
    list  all games in the dynamodb
    :return: list contains game data
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')

    response = table.scan()

    records = []

    for i in response['Items']:
        i['amazon_link'] = 'https://www.amazon.ca/s?k='+i['Name'].replace(' ','+')+'+ps4'
        records.append(i)
    return records

def update_new_game (game_name,img,price,date,link):
    '''
    add game data into new games table in dynamodb
    '''
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

def update_will_free_game (game_name,img,price,date,link):
    '''
        add game data into free games table in dynamodb
    '''
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


def update_will_release_game (game_name,img,price,date,link):
    '''
        add game data into upcoming games table in dynamodb
    '''
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
    '''
    list all games stored in new game
    :return: list contains games data
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('New_game')

    response = table.scan()

    records = []
    for i in response['Items']:
        i['amazon_link'] = 'https://www.amazon.ca/s?k='+i['Name'].replace(' ','+')+'+ps4'
        records.append(i)
    records.sort(key=lambda k: (k.get('date', 0)),reverse=True)
    return records

def list_all_free_games():
    '''
    list all games stored in free game
    :return: list contains games data
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Free_games')

    response = table.scan()

    records = []
    for i in response['Items']:
        i['amazon_link'] = 'https://www.amazon.ca/s?k='+i['Name'].replace(' ','+')+'+ps4'
        records.append(i)
    return records

def list_all_will_release_games():
    '''
    list all games stored in will release game
    :return: list contains games data
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Will_release_games')

    response = table.scan()

    records = []
    for i in response['Items']:
        i['amazon_link'] = 'https://www.amazon.ca/s?k='+i['Name'].replace(' ','+')+'+ps4'
        records.append(i)
    records.sort(key=lambda k: (k.get('date', 0)), reverse=False)
    return records

def list_search_results(search_txt):
    '''
    search games in the dynamodb
    :param search_txt: user input
    :return: list of searched games
    '''
    table_name ='PS4_games'

    response = search_name(search_txt,table_name)

    records = []
    for i in response['Items']:
        i['amazon_link'] = 'https://www.amazon.ca/s?k='+i['Name'].replace(' ','+')+'+ps4'
        records.append(i)
    return records

def delete_all_new():
    '''
    delete games in new game table
    '''
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
    '''
    delete games in free game table
    '''
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
    '''
    delete games in upcoming game table
    '''
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
    '''
    search game in the dynamodb
    :param text_search: user input
    :param table_name: search table
    :return:
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression= Attr("Name").contains(text_search))
    for i in response['Items']:
        print(i)

    return response

def fuzzy_search(text_search,type='Name'):
    '''
    search games with name likely to user input
    :param text_search: user input
    :param type: search name of game
    :return:
    '''
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
    for i in records:
        i['amazon_link'] = 'https://www.amazon.ca/s?k=' + i['Name'].replace(' ', '+') + '+ps4'
    return records

def image_detect(file_key):
    '''
    call aws rekognition to create image's tag
    :param file_key: key value in S3
    :return: tag of the img
    '''
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
    '''
    detect text in the image by using aes rekognition
    :param file_key: key value in S3
    :return: text in the img
    '''
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
    '''
    add detected tag of img into dynamodb
    '''
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
    '''
    add detected text into dynamodb
    '''
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
    '''
    search games by text in it
    :param text_search: text in image
    :return: list of search result
    '''
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
    '''
    search game by genre of upload image
    :param tmp_key: key of upload image
    :return: list of search result
    '''
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