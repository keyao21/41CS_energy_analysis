import urllib.request
import json 
import pandas as pd




# for index, row in data.iterrows():
#     print( row[0], row[1], row[-1])

data =  {
        "Inputs": {
                "input1": {
                    "ColumnNames": ["DATE", "DB", "WB", "Hour", "Minute", "Day", "Weekend", "Utility Subtotal", "DateMonth", "DateDay"],
                    "Values": [ 
                                [ "2016-12-31T21:00:00", "0", "0", "0", "0", "0", "0", "0", "0", "0" ], 
                                [ "2016-12-31T21:00:00", "1", "100", "0", "100", "100", "0", "0", "0", "0" ] 
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
    # print(json.dumps(result, indent=2))

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    print(error.info())

