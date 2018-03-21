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

def query_powerdash_recent(elapsed_min, board_name):
	elapsed = (60*1000)*elapsed_min
	payload = {'elapsed': elapsed, 'dgm': powerdash_info.powerdash_name_to_dgm[board_name],
	           'format': 'csv'}
	data = 	requests.get(url=powerdash_info.powerdash_base_url + "/recent", params=payload)
	if data == "":
		return None
	return StringIO(data.text)

def get_prediction(weather_data):
	DATE = weather_data[0]
	DB = weather_data[1]
	WB = weather_data[2]
	Hour = weather_data[3]
	Minute = weather_data[4]
	Day = weather_data[5]
	Weekend = weather_data[6]
	DateMonth = weather_data[7]
	DateDay = weather_data[8]

	testDate = "{:%Y-%m-%dT%H:%M:%S}".format(datetime.now())
	test_data = [ testDate, str(int(DB)), str(int(WB)), str(Hour), str(Minute), str(Day), str(Weekend), str(DateMonth), str(DateDay), "0" ]
	# test_data2 = ['3/20/2018 6:43:03 PM', '40', '32', '18', '1063', '2', '0', '3', '20', '0']
	# test_data3 = ['3/20/2018 8:43:03 PM', '36', '32', '20', '1063', '2', '0', '3', '20', '0']

	data =  {
	        "Inputs": {
	                "input1": {
	                    "ColumnNames": ["DATE", "DB", "WB", "Hour", "Minute", "Day", "Weekend", "DateMonth", "DateDay", "Utility Subtotal"],
	                    "Values": [ 
	                                test_data 
	                                # test_data2, 
	                                # test_data3
	                              ]
	                        },        
	                },
	}

	body = str.encode(json.dumps(data))
	url = 'https://ussouthcentral.services.azureml.net/workspaces/791b6dabd0fd4b96ba1f7010bdd78f34/services/36b3b2c080774dd285f80a9e5cd944fe/execute?api-version=2.0&details=true'
	api_key = 'ZEhISw58bTm2tnM4Nxy6vxwtQQjVDbpKaPy2CdZym+Z77Tn4etaQCzcHa5biDezXA7bC+wRGUSfkqh/YfRJX9Q==' # Replace this with the API key for the web service
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	req = urllib.request.Request(url, body, headers)  
	try:
	    response = urllib.request.urlopen(req)
	    # encoding = urllib.request.get_content_charset()
	    # result = json.loads(response.read().decode(encoding))
	    # encoding = urllib.request.headers.get_content_charset()
	    # result = response.read().decode(encoding)
	    result = response.read().decode('utf8').replace("'", '"')
	    # print(result)
	    result = json.loads(result)
	    # result = json.dumps(result, indent=2)
	    # print(result['Results'])
	    # print(result['Results'])
	    results = result['Results']
	    # print( results['output1'] )
	    for output in results:
	    	# print(results[output]['value']['Values'])
	    	return results[output]['value']['Values'][0]



	except urllib.error.HTTPError as error:
	    print("The request failed with status code: " + str(error.code))
	    print(error.info())

if __name__ == '__main__':
	# print(query_powerdash_recent(elapsed_min=2, board_name='overall utilities'))
	while(True):
		weather_data = weatherResponse()
		print(get_prediction(weather_data))
		ptime.sleep(5)
