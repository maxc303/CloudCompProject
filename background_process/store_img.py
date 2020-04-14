import requests

import app.utils as u
import boto3, os
if __name__ == '__main__':
    records = u.list_all()
    for record in records:
        url = record['img']
        name = record['Name']
        response = requests.get(url)
        with open('./a.jpeg', 'wb') as f:
            f.write(response.content)
        s3 = boto3.resource('s3')
        key = 'dynamo/'+name+'.jpeg'
        s3.meta.client.upload_file('./a.jpeg', 'ps4img', key)
        os.remove('./a.jpeg')
        print(name,' uploaded')
