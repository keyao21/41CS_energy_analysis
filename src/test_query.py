import json
from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
import powerdash_info
import requests
import matplotlib.pyplot as plt
import time as ptime



def query_powerdash_recent(elapsed_min, board_name):
	elapsed = (60*1000)*elapsed_min
	payload = {'elapsed': elapsed, 'dgm': powerdash_info.powerdash_name_to_dgm[board_name],
	           'format': 'csv'}
	data = 	requests.get(url=powerdash_info.powerdash_base_url + "/recent", params=payload)
	if data == "":
		return None
	return StringIO(data.text)
	

if __name__ == '__main__':
	elapsed_min =  10# minutes passed
	board_name = 'overall utilities'
	csv_data = query_powerdash_recent(elapsed_min, board_name)
	data = pd.read_csv(csv_data)
	print(data[['time', 'Total KW']])

