import urllib.request
import json 
import pandas as pd

# testing query for recent data
import test_query
elapsed_min =  1 # minutes passed
board_name = 'roof mechanical'
csv_data = test_query.query_powerdash_recent(elapsed_min, board_name)
data = pd.read_csv(csv_data)
print(data)


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

# testing ml pipe
test_data = [ "2016-12-31T21:00:00", str(int(DB)), str(int(WB)), str(Hour), str(Minute), str(Day), str(Weekend), "value" ]
print( test_data )
data =  {
        "Inputs": {
                "input1": {
                    "ColumnNames": ["DATE", "DB", "WB", "Hour", "Minute", "Day", "Weekend", "Utility Subtotal"],
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
    result = response.read()
    print(result)
    #  print(json.dumps(result, indent=2))

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    print(error.info())




