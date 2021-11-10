from kafka import KafkaConsumer
from pymongo import MongoClient

MONGO_HOST= 'mongodb://host:27017/twitter_db'

client = MongoClient(MONGO_HOST)
db = client.twitter_db
consumer = KafkaConsumer(
	'twitter-topic',
	bootstrap_servers = ['kafka_server:9092'])


for message in consumer:
	# e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value.decode("utf-8")))

    #crear json de información con la información capturada para la base de datos 
    data_dict = {
    	'topic': message.topic,
    	'partition': message.partition,
    	'offset': message.offset,
    	'key': message.key,
    	'value': message.value.decode("utf-8"),
    }

    db.tweets_analisys.insert_one(data_dict)
