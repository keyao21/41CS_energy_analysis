import json
from urllib import request
import numpy as np
from datetime import datetime


def weatherResponse():

	from urllib import request
	url = "http://api.wunderground.com/api/df3fe28d0415281a/conditions/q/ny/newyork.json"
	request = request.urlopen(url)
	encoding = request.headers.get_content_charset()
	data = json.loads(request.read().decode(encoding))
	print (json.dumps(data,indent=2))

	variables = {
		'temp_f',
		'temp_c',
		'dewpoint_f',
		'dewpoint_c',
		'relative_humidity',
		'pressure_mb'
	}


	# mapper for datetime.now().weekday()
	weekday_mapper = {
		1:'Monday',
		2:'Tuesday',
		3:'Wednesday',
		4:'Thursday',
		5:'Friday',
		6:'Saturday',
		7:'Sunday'
	}

	# get current date
	print("\nCURRENT DATE")
	print('DATE:', datetime.now())
	print('HOUR:', datetime.now().hour)
	print('MINUTE:', datetime.now().minute)
	print('DAY:', weekday_mapper[datetime.now().weekday()])
	print('WEEKEND:', 1 if datetime.now().weekday()==6 or datetime.now().weekday()==6 else 0)

	# pull wanted parameters
	print("\nALL PULLED PARAMETERS:")
	pulled_data = dict()
	for var in variables:
		print( '{}: {}'.format(var, data['current_observation'][var]))
		pulled_data[var] = data['current_observation'][var]

	# set known parameters
	rel_hum = float(pulled_data['relative_humidity'].strip('%'))
	dewpoint_c = float(pulled_data['dewpoint_c'])

	const = np.log(100/rel_hum) + (1.8096+((17.2694*dewpoint_c)/(237.3+dewpoint_c))) - 1.8096
	dry_bulb_c = const*237.3/(17.2694-const)

	print('\nPULLED PARAMETERS')
	print('rel_hum:', rel_hum)
	# print(const)
	print('dry_bulb_c:', dry_bulb_c )


	pressure_mb = float(pulled_data['pressure_mb'])

	vapor_pressure = (6.11 * 10**(7.5 * dewpoint_c / (237.7 + dewpoint_c)))
	wet_bulb_c = (((0.00066 * pressure_mb) * dry_bulb_c) + ((4098 * vapor_pressure) / ((dewpoint_c + 237.7)**2) * dewpoint_c)) / \
					((0.00066 * pressure_mb) + (4098 * vapor_pressure) / ((dewpoint_c + 237.7)**2))

	# print(dewpoint_c)
	print('\nDERIVED PARAMETERS')
	print('vapor_pressure:', vapor_pressure)
	print('web_bulb_c:', wet_bulb_c)



	# return format
	# ["DATE", "DB", "WB", "Hour", "Minute", "Day", "Weekend"]
	DATE = datetime.now()
	DB = dry_bulb_c
	WB = wet_bulb_c
	Hour = datetime.now().hour
	Minute = datetime.now().minute
	Day = weekday_mapper[datetime.now().weekday()]
	Weekend = 1 if datetime.now().weekday()==6 or datetime.now().weekday()==6 else 0

	print([DATE, DB, WB, Hour, Minute, Day, Weekend])

if __name__ == '__main__':
	weatherResponse()
