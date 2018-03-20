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
	def __init__(self, duration, filename):
		self.duration = duration
		self.filename = filename
		self.queue = pd.DataFrame(columns=['Time', 'Actual', 'Predicted'])
	def append(self, time, actual, predicted):
		if self.queue.shape[0]==self.duration:
			self.queue.drop(self.queue.head(1).index, inplace=True)
		newData = pd.DataFrame([[time, actual, predicted]], columns=['Time', 'Actual', 'Predicted'])
		self.queue = self.queue.append(newData, ignore_index=True)





