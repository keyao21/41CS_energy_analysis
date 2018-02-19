import pandas as pd
import datetime as datetime
import matplotlib.pyplot as plt
import os

fig, axs = plt.subplots(11,1, figsize=(15, 6), facecolor='w', edgecolor='k')

directory = 'distribution_board_data/'
for dirname, directories, filenames in os.walk(directory):
    for filename in filenames:
        print( filename )
  
          

        data = pd.read_csv("{}{}".format(directory, filename), header=None)
        data.columns = ['Datetime', 'Energy']
        data['Datetime'] = pd.to_datetime(data['Datetime'])
        data['Date'] = data['Datetime'].apply(lambda x: x.date())
        data['Time'] = data['Datetime'].apply(lambda x: x.time())
        data['year'] = data['Datetime'].apply(lambda x: x.year)     
        data['month'] = data['Datetime'].apply(lambda x: x.month)
        data['day'] = data['Datetime'].apply(lambda x: x.day)
        data['hour'] = data['Datetime'].apply(lambda x: x.hour)

        daily_average = data.groupby('Date').mean()

        # plt.figure()
        daily_average['Energy'].plot()
        axs.set_title("Daily Average Use of {}".format(filename[:-4]) )
        axs.ylabel("Energy Usage")
        axs.show()



{
'3rd floor lighting and plugs',
'4th floor lighting and plugs',
'4th floor mechanical 2nd,3rd,5th lighting and plugs',
'6th floor lighting and plugs',
'7th floor lighting and plugs',
'7th floor mechanical, 8th and 9th lighting and plugs',
'cellar power and lighting',
'elevator',
'retail',
'roof mechanical',
'sub-cellar power and lighting'  }