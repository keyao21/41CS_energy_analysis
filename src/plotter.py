from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
import powerdash_info
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
plt.style.use('ggplot')
import numpy as np
import time as ptime
import json 
import urllib.request
from wunderground_response import weatherResponse
from utils import *
import threading


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


def streamData(test=False, duration=30):
	print("Initiating Cache")
	cache = Cache(duration=duration, filename='test.csv')
	start_time = ptime.time()
	count = 0
	summ = 0	
	while(True):
		current_time = format(ptime.time()-start_time, '2.2f')
		print("-----------------------------------------")
		start = ptime.time()
		actual_data = get_actual_data()
		weather_data = weatherResponse()
		if test:
			data_package = {
				'time'      : datetime.now(),
				'actual'    : actual_data['Total KW'],
				'predicted' : get_prediction(weather_data)[-1]
			}
		else:
			data_package = {
				'time'      : actual_data['time'],
				'actual'    : actual_data['Total KW'],
				'predicted' : float(get_prediction(weather_data)[-1])*(7/8)
			}
		end = ptime.time()-start
		print('waittime: {0:>5.2f} seconds'.format(end))
		summ += end
		count += 1
		print('average : {0:>5.2f} seconds'.format(summ/count))
		print('data: ', data_package)
		print('appending to cache...')
		cache.appendToQueue(data_package['time'], 
							data_package['actual'], 
							data_package['predicted'])
		print('added to cache!')
		print('\n\nCURRENT CACHE:\n')
		print( cache.queue )
		print('\n-----------------------------------------')
		ptime.sleep(5)

def plot():
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        dataframe = pd.read_csv('test.csv', engine='c')
        dataframe.Time = dataframe.Time.apply(lambda x: pd.to_datetime(x))
        dataframe = dataframe.set_index('Time')
        print( dataframe )
        dataframe = dataframe.sort_index()
        predict = dataframe['Predicted']
        actual = dataframe['Actual']

        window = 5

        ma = predict.rolling(window).mean()
        mstd = predict.rolling(window).std()

        dataframe['signal'] = np.sign(abs(actual-ma)-2*mstd)
        markers = dataframe[ dataframe.signal > 0 ]['Actual']

        ax1.clear()
        ax1.plot(actual.index, actual, label='Actual Value', color='b')
        ax1.fill_between(mstd.index, ma-2*mstd, ma+2*mstd, color='b', alpha=0.2)
        ax1.scatter(markers.index, markers, facecolors='none', edgecolors='r', label='Fault Detected')

        handles, labels = ax1.get_legend_handles_labels()
        color_block = mpatches.Patch(color='b', alpha=0.2)
        display = [0,1]

        ax1.set_title('Fault Detection for Overall Energy Usage')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('kWh')
        ax1.legend( [handle for i,handle in enumerate(handles) if i in display]+[color_block],
                  [label for i,label in enumerate(labels) if i in display]+['Predicted Range'] )
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()


def testThreading():
	t1 = threading.Thread(target=plot)
	t2 = threading.Thread(target=streamData)

	t1.start()
	t2.start()

if __name__ == '__main__':
	streamData(duration=30)

# if __name__ == '__main__':
# 	# streamData(test=False)
# 	testThreading()

	