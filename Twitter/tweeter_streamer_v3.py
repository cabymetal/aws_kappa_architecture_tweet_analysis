
from tweepy import OAuthHandler, Stream, API, Cursor

import app_credentials
import msgpack
import os
import re
import sys
import time
from tqdm import tqdm
import pdb
import json
import unidecode as ud

import boto3



class StdOutListener(Stream):
	def __init__(self, ckey, conkey, atok, atoksec, time_limit, stream_name, kinesis_client):
		super(StdOutListener, self).__init__(ckey, conkey, atok, atoksec)
		self.start_time = time.time()
		self.limit = time_limit
		self.id = 0
		self.stream_name = stream_name
		self.kinesis_client = kinesis_client

	def on_status(self, status):
		if (time.time() - self.start_time) <= self.limit:
			#logica para transformar tweets
			tweet_dict = {
				'id'			: self.id,
				'text' 			: ud.unidecode(status.text),
				'created_time'	: status.created_at.isoformat(),
				'source'		: status.source,
				'tweet_id'		: status.id_str,
				'user_name'		: status.user.name,
				'user_id'		: status.user.id_str,
				'run_start_time': self.start_time,
				'run_time_limit': self.limit
			}

			self.send_to_kinesis(self.stream_name, self.kinesis_client, tweet_dict)


			self.id = self.id + 1
		else:
			self.disconnect()

	def on_connection_error(self):
		self.disconnect()

	def send_to_kinesis(self, stream_name, kinesis_client, tweet_dict):
		data = tweet_dict
		kinesis_client.put_record(
			StreamName=stream_name,
			Data=json.dumps(data),
			PartitionKey="partitionkey")



def background(stream):
	stream.filter(track = ['quinterocalle', 'medellin', 'alcalde'],
	 languages = ['en', 'es'], threaded=True)

def wait(minutes):
	for i in tqdm(range(int(60*minutes - 1))): # termine antes que aparezca el mensaje de finalización de conexión
		time.sleep(1)  #update each second


if __name__ == '__main__':
	MINUTES = 60
	stream_name, kinesis_client = 'new_twitter_stream', boto3.client('kinesis')

	listener = StdOutListener(app_credentials.CONSUMER_KEY, app_credentials.CONSUMER_SECRET,
		app_credentials.ACCESS_TOKEN, app_credentials.ACCESS_TOKEN_SECRET,
		60*MINUTES, stream_name, kinesis_client)


	try:
		background(listener)
		wait(MINUTES)
	except Exception as e:
		print(e)
	finally:
		listener.disconnect()

	#finaliza ejecucion
	print("Ejecución terminada")