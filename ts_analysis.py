import pandas as pd
from datetime import datetime
import get_clean_data as Data
import matplotlib.pyplot as plt
import os
'''
This is some exploratory time series analysis 
'''

def getData(overall=True, start=1483241304000, end=1506828504000):
    # get data from server 
    # start = 1483241304000 # 1/1/17
    # end   = 1506828504000 # 9/30/17 
    if overall:
        data = Data.get_overall(start=start, end=end)
        data = pd.DataFrame(data)
    else:
        data = Data.get_distribution_boards(start=start, end=end)
    return data


def getTS(filename=None, from_memory=True, overall=True, start=1483241304000, end=1506828504000):
    # get csv data ts file from current directory
    if from_memory and filename:            
        ts = pd.read_csv(filename)
    else:
        ts = getData(overall, start, end)
    if overall:
        ts['time'] = pd.to_datetime(ts['time'])
        ts['year'] = ts['time'].apply(lambda x: x.year)     
        ts['month'] = ts['time'].apply(lambda x: x.month)
        ts['day'] = ts['time'].apply(lambda x: x.day)
        ts['hour'] = ts['time'].apply(lambda x: x.hour)
        ts['min'] = ts['time'].apply(lambda x: x.minute)

    return ts


def compareNightDay(filename, overall=True, start=1483241304000, end=1506828504000):
    '''
    Given the time series with a datetime index, 
    find the difference between night (12:00 am) and 
    day (12:00 pm) time series values
    ''' 
    if overall:
        ts = getTS(filename, overall=True, start=start, end=end)
        ts = ts.loc[((ts['hour']==0) | (ts['hour']==12))  & (ts['min']==0) ]  
        ts = ts.groupby(['month', 'day', 'hour', 'min']).mean()
        ts = ts.reset_index()
        ts = pd.merge(ts.loc[ts['hour']==12], 
            ts.loc[ts['hour']==0], how='inner', on=['year','month', 'day'])
        ts.index = pd.to_datetime(ts[['year', 'month', 'day']])

        modes = { 'SV2KW_{}', 'SRV1KW_{}', 'SV2PKW_{}', 'Total KW_{}', 'SRV1PKW_{}',
               'CU_TOT_KW_{}'}

        for mode in modes:
            day, night = ts[mode.format('x')], ts[mode.format('y')] 
            plt.figure()
            plt.title(mode[:-3])
            plt.plot(day)
            plt.plot(night)
            # plt.axis(pd.to_datetime(ts[['year', 'month', 'day']]))
            plt.savefig('plots/overall_utilities/{}.pdf'.format(mode[:-3]), format='pdf')
            diff = day - night
            print( '\n{}'.format(mode[:-3]))
            print( diff.describe() )
            print( '\n=====================')
    else:
        # get distribution boards (not overall)
        # start = 1500828504000
        # end = 1506828504000
        # FOR NOW WE WILL USE PREDOWNLOADED DATA
        for dirname, subdir, filenames in os.walk('distribution_board_data'):
            for filename in filenames:
                print( filename )
                ts = pd.read_csv('distribution_board_data/{}'.format(filename), header=None)
                ts[0] = pd.to_datetime(ts[0])

                ts['year'] = ts[0].apply(lambda x: x.year)     
                ts['month'] = ts[0].apply(lambda x: x.month)
                ts['day'] = ts[0].apply(lambda x: x.day)
                ts['hour'] = ts[0].apply(lambda x: x.hour)
                ts['min'] = ts[0].apply(lambda x: x.minute)

                ts = ts.loc[((ts['hour']==0) | (ts['hour']==12))  & (ts['min']==0) ]  
                ts = ts.groupby(['month', 'day', 'hour', 'min']).mean()
                ts = ts.reset_index()
                ts = pd.merge(ts.loc[ts['hour']==12], 
                    ts.loc[ts['hour']==0], how='inner', on=['year','month', 'day'])

                ts.index = pd.to_datetime(ts[['year', 'month', 'day']])
                day, night = ts['1_{}'.format('x')], ts['1_{}'.format('y')]
                board = filename[:-4]
                plt.figure()
                plt.plot(day)
                plt.plot(night)
                plt.title(board)
                plt.savefig('plots/distribution_boards/{}.pdf'.format(board), format='pdf')
                diff = day - night
                print( '\n{}'.format(board))
                print( diff.describe() )
                print( '\n=====================')

        plt.show()



    return 0

def compareWeekends():
    '''
    Given the time series with a datetime index, 
    find the difference between weekends and 
    weekdays time series values
    '''
    pass

def compareWeather():
    '''
    Given the time series with a datetime index, 
    compare with parallel weather data
    '''
    pass

if __name__ == "__main__":
    # plt.close('all')
    filename = 'THIS_YEAR.csv'
    compareNightDay(filename, overall=False)


