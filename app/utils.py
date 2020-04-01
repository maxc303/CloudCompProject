import boto3


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

def update_amz_price(game_name,new_price):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PS4_games')
    first_char = game_name[0]
    table.update_item(

        Key = {
              'FirstChar': first_char,
              'Name': game_name
          },
    UpdateExpression = 'SET Amazon_price= :val1',
    ExpressionAttributeValues = {
        ':val1': 26
    }
    )




if __name__ == "__main__":
    ##put_item('test1','fps','/')
    update_amz_price('test1',1)
