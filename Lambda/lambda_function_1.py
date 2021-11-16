#importar librerías
import os
import boto3
import base64
import json
import decimal
import datetime
from datetime import datetime

def lambda_handler(event, context):
    #importar clientes y recursos disponibles en boto3
    dynamo_db = boto3.resource('dynamodb')
    comprehend =  boto3.client(service_name = 'comprehend')
    s3 = boto3.resource('s3')
    kinesis_client, stream_name = boto3.client('kinesis'), 'sentiment-outputstream'
    table = dynamo_db.Table('tweets_for_sentiment')
    table_sentiments = dynamo_db.Table('tweets_sentiment')
    #parsear la información recibida de kinesis
    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]
    #iterar por cada registro de kinesis
    for item in deserialized_data:
      id_exec       =   item['id']
      text          =   item['text']
      created_time  =   item['created_time']
      source        =   item['source']
      tweet_id      =   item['tweet_id']
      user_name     =   item['user_name']
      user_id       =   item['user_id']
      run_start_time=   item['run_start_time']
      run_time_limit=   item['run_time_limit']
      
      sentiment_all = comprehend.detect_sentiment(Text = text, LanguageCode = 'es')
      sentiment = sentiment_all['Sentiment']
      
      #información para la tabla de Dynamo de almacenamiento de tweets
      dict_tweet = {
              'id'            :   tweet_id,
              'id_exec'       :   id_exec,
              'text'          :   text,
              'created_time'  :   created_time,
              'source'        :   source,
              'user_name'     :   user_name,
              'user_id'       :   user_id,
              'run_start_time':   decimal.Decimal(run_start_time),
              'run_time_limit':   run_time_limit,
      }
      #información para la tabla de Dynamo de almacenar sentimientos
      dict_sentiment_ = {
        'id'            :   tweet_id,
        'text'          :   text,
        'created_time'  :   created_time,
        'user_name'     :   user_name,
        'sentiment'     :   sentiment,
        'score_positive':   sentiment_all['SentimentScore']['Positive'],
        'score_negative':   sentiment_all['SentimentScore']['Negative'],
        'score_neutral' :   sentiment_all['SentimentScore']['Neutral'],
        'score_mixed'   :   sentiment_all['SentimentScore']['Mixed']
      } # data to send through kinesis
      
      dict_sentiment = {
        'id'            :   tweet_id,
        'text'          :   text,
        'created_time'  :   created_time,
        'user_name'     :   user_name,
        'sentiment'     :   sentiment,
        'score_positive':   decimal.Decimal(sentiment_all['SentimentScore']['Positive']),
        'score_negative':   decimal.Decimal(sentiment_all['SentimentScore']['Negative']),
        'score_neutral' :   decimal.Decimal(sentiment_all['SentimentScore']['Neutral']),
        'score_mixed'   :   decimal.Decimal(sentiment_all['SentimentScore']['Mixed'])
      }# data to send to dynamo
      
      #data que será recibida en "tiempo real" por logstash y kibana
      kinesis_client.put_record(
			  StreamName=stream_name,
			  Data=json.dumps(dict_sentiment_),
			  PartitionKey="sentimentpartitionkey"
			)
      
      #enviar datos a Kinesis
      with table.batch_writer() as batch_writer:
        # write to dynamo
        batch_writer.put_item(
          Item = dict_tweet
        )
        
      with table_sentiments.batch_writer() as batch_writer:
        batch_writer.put_item(
          Item = dict_sentiment
        )
      
      #todo write to csv and put on s3 '¿how to do this in a feasible forma?'
      
      
    
    # esto no es importante se puede borrar
    return {
      "statusCode": 200,
      "body": "\"Hello from Lambda!\""
    }