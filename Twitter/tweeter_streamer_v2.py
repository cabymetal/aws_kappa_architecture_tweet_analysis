
from tweepy import OAuthHandler, Stream, API, Cursor

import app_credentials
import msgpack
import os
import re
import sys
import time
from tqdm import tqdm
import pdb

from kafka import KafkaProducer
from kafka.errors import KafkaError

class MyKafkaProducer(KafkaProducer):
	def __init__(self, server):
		super(MyKafkaProducer, self).__init__(bootstrap_servers=[server])

	def on_send_success(self, record_metadata):
		print("mensaje enviado a :" + record_metadata.topic)
		print(record_metadata.partition)

	def on_send_error(self, kafka_exception):
		print("error de kafka: " + kafka_exception)




class StdOutListener(Stream):
	def __init__(self, ckey, conkey, atok, atoksec, time_limit, kafka_producer):
		super(StdOutListener, self).__init__(ckey, conkey, atok, atoksec)
		self.start_time = time.time()
		self.limit = time_limit
		self.id = 0
		self.kafka_producer = kafka_producer

	def on_status(self, status):
		if (time.time() - self.start_time) <= self.limit:
			self.kafka_producer.send('twitter-topic', key = bytes(str(self.id), encoding='latin'), 
				value = bytes(status.text, encoding = 'utf-8'))
			#	.add_callback(self.kafka_producer.on_send_success).add_errback(self.kafka_producer.on_send_error)
			#print(status.text, self.id)
			self.id = self.id + 1
		else:
			self.disconnect()

	def on_connection_error(self):
		self.disconnect()



def background(stream):
	stream.filter(track = ['Covid', 'football', 'soccer', 'Madrid', 'Mbappe'],
	 languages = ['en', 'es'], threaded=True)

def wait(minutes):
	for i in tqdm(range(int(60*minutes - 1))): # termine antes que aparezca el mensaje de finalización de conexión
		time.sleep(1)  #update each second


if __name__ == '__main__':
	MINUTES = 1
	kafka_producer = MyKafkaProducer('url_kafka_consumer:portnumber') #defaul 9092


	listener = StdOutListener(app_credentials.CONSUMER_KEY, app_credentials.CONSUMER_SECRET,
		app_credentials.ACCESS_TOKEN, app_credentials.ACCESS_TOKEN_SECRET,
		60*MINUTES, kafka_producer)


	try:
		background(listener)
		wait(MINUTES)
	except Exception as e:
		print(e)
	finally:
		listener.disconnect()

	#finaliza ejecucion
	print("Ejecución terminada")
