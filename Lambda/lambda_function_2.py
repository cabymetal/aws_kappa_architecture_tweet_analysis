import json
import base64
import boto3
import csv
import unidecode as ud
from datetime import datetime
from botocore.errorfactory import ClientError


#tomar la fecha de ejecución actual
now = datetime.now()
year, month, day, hour = now.year, now.month, now.day, now.hour

def lambda_handler(event, context):
    
    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]
    
    key = f'tweets_json/{year}/{month}/{day}/{hour}/tweets.csv'
    local_file_name = '/tmp/test.csv'
    #trandforma registros de Kinesis en una archivo csv que se almacena en un formato similar al que se 
    #utiliza en firehose por defecto pero en formato csv no JSON
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    try:
        s3.head_object(Bucket='rawcmurill5', Key=key)
        # download s3 csv file to lambda tmp folder
        s3_resource.Bucket('rawcmurill5').download_file(key,local_file_name)
        with open(local_file_name, 'a', newline='') as outfile:
            writer = csv.writer(outfile, delimiter= ';' )
            for data in deserialized_data:
                dict = {}
                for k, v in data.items():
                    if isinstance(v, str):
                        dict[k] = ud.unidecode(v)
                    else:
                        dict[k] = v
                    
                writer.writerow(dict.values())
    except ClientError:
        with open(local_file_name, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter= ';' )
            writer.writerow(deserialized_data[0].keys())
            for data in deserialized_data:
                dict = {}
                for k, v in data.items():
                    if isinstance(v, str):
                        dict[k] = ud.unidecode(v)
                    else:
                        dict[k] = v
                    
                writer.writerow(dict.values())
        pass
    
    # upload file from tmp to s3 key
    
    
    bucket = s3_resource.Bucket('rawcmurill5')
    bucket.upload_file('/tmp/test.csv', key)
    
    return deserialized_data
