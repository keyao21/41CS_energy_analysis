import urllib.request
import json 
import pandas as pd
from datetime import datetime 


# testing query for recent data
import test_query
elapsed_min = 2# minutes passed
board_name = 'overall utilities'
csv_data = test_query.query_powerdash_recent(elapsed_min, board_name)
data = pd.read_csv(csv_data)
data = data[['time', 'Total KW']]
print(data.iloc[-1])

# testing wunderground weather response data
from wunderground_response import weatherResponse
weather_data = weatherResponse()
DATE = weather_data[0]
DB = weather_data[1]
WB = weather_data[2]
Hour = weather_data[3]
Minute = weather_data[4]
Day = weather_data[5]
Weekend = weather_data[6]
DateMonth = weather_data[7]
DateDay = weather_data[8]

# print(DATE)
testDate = "{:%Y-%m-%dT%H:%M:%S}".format(datetime.now())
# testing ml pipe
test_data = [ testDate, str(int(DB)), str(int(WB)), str(Hour), str(Minute), str(Day), str(Weekend), str(DateMonth), str(DateDay), "0" ]
# print( test_data )
data =  {
        "Inputs": {
                "input1": {
                    "ColumnNames": ["DATE", "DB", "WB", "Hour", "Minute", "Day", "Weekend", "DateMonth", "DateDay", "Utility Subtotal"],
                    "Values": [ 
                                test_data 
                              ]
                        },        
                },
        # "GlobalParameters": {
    # }
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
    	print(results[output]['value']['Values'])



except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    print(error.info())




