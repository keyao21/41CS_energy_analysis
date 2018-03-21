from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
import powerdash_info
import requests
import matplotlib.pyplot as plt
import time as ptime
import json 
import urllib.request
from wunderground_response import weatherResponse
from utils import *

class Cache():
	def __init__(self, duration, filename=None):
		self.duration = duration
		self.filename = filename
		self.queue = pd.DataFrame(columns=['Time', 'Actual', 'Predicted'])
	def appendToQueue(self, time, actual, predicted):
		if self.queue.shape[0]==self.duration:
			self.queue.drop(self.queue.head(1).index, inplace=True)
		newData = pd.DataFrame([[time, actual, predicted]], columns=['Time', 'Actual', 'Predicted'])
		self.queue = self.queue.append(newData, ignore_index=True)
		if self.filename:
			self.queue.to_csv(self.filename)

def get_actual_data():
	csv_data = query_powerdash_recent(elapsed_min=2, board_name='overall utilities')
	data = pd.read_csv(csv_data)
	return data[['time', 'Total KW']].iloc[-1]


def test_latency():
	# at cooper it takes about 0.5 seconds to get information
	print("Initiating Cache")
	cache = Cache(duration=3, filename='test.csv')
	start_time = ptime.time()
	count = 0
	summ = 0	
	while(True):
		current_time = format(ptime.time()-start_time, '2.2f')
		print("-----------------------------------------")
		start = ptime.time()
		actual_data = get_actual_data()
		weather_data = weatherResponse()
		predict_data = get_prediction(weather_data)[-1]
		end = ptime.time()-start
		print('took {0:2.2f} seconds'.format(end))
		summ += end
		count += 1
		print('current avg:  {0:2.2f}'.format(summ/count))


def updateCache():
	print("Initiating Cache")
	cache = Cache(duration=3, filename='test.csv')
	start_time = ptime.time()
	count = 0
	summ = 0	
	while(True):
		current_time = format(ptime.time()-start_time, '2.2f')
		print("-----------------------------------------")
		start = ptime.time()
		actual_data = get_actual_data()
		weather_data = weatherResponse()
		predict_data = get_prediction(weather_data)[-1]
		end = ptime.time()-start
		print('took {0:2.2f} seconds'.format(end))
		summ += end
		count += 1
		print('current avg:  {0:2.2f}'.format(summ/count))
		print('data: ', (actual_data['time'], actual_data['Total KW'], predict_data))
		ptime.sleep(15*60)

if __name__ == '__main__':
	updateCache()

	