# combine weather data with cooper data
import pandas as pd
import numpy as np
import ftplib 


ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
ftp.login()
ftp.cwd('pub/data/ghcn/daily/by_year')
ftp.retrbinary("RETR " + '2018.csv.gz', open('../data/weather_data/2018.csv.gz', 'wb').write)

# weather_data = pd.read_csv('../data/weather_data/2018.csv.gz', header=None)

def weatherData(year):
    weather_data = pd.read_csv('../data/weather_data/{}.csv.gz'.format(year), 
                               header=None,
                               index_col=False,
                               names=['station_identifier', 
                                      'measurement_date', 
                                      'measurement_type', 
                                      'measurement_flag', 
                                      'quality_flag', 
                                      'source_flag', 
                                      'observation_time'],
                               parse_dates=['measurement_date'])

    nyc_data = weather_data[ weather_data.station_identifier=='USW00094728' ].set_index('measurement_date')
    temp_data = pd.DataFrame(columns=['TMAX', 'TMIN', 'TAVG'])
    temp_data['TMAX'] = nyc_data.loc[ nyc_data.measurement_type=='TMAX', 'measurement_flag' ].rename('TMAX')
    temp_data['TMIN'] = nyc_data.loc[ nyc_data.measurement_type=='TMIN', 'measurement_flag' ].rename('TMIN')
    temp_data['TAVG'] = temp_data.mean(axis=1)

    temp_data = (temp_data/10)*(9/5) + 32  # convert to farenheit
    return temp_data


weatherData(2018).to_csv('../data/weather_data/2018_weather.csv')

weather_data = pd.read_csv('../data/weather_data/2018_weather.csv')
cooper_data = pd.read_csv('../data/test_overall.csv')
# cooper_data = pd.read_csv('CU_UtilityData_ky_2016.csv')

# just take wet bulb and dry bulb hourly data
weather_data = weather_data[['DATE','HOURLYDRYBULBTEMPF','HOURLYWETBULBTEMPF']]
weather_data.columns = ['time', 'DB', 'WB']
weather_data.time = pd.to_datetime(weather_data.time)
weather_data.time = weather_data.time.map( lambda t: t.strftime('%Y-%m-%d %H:%M:00'))
weather_data.time = pd.to_datetime(weather_data.time)


# just take subtotal
# cooper_data = cooper_data[['time', 'Total KW']]
# cooper_data.columns = ['time', 'Utility Subtotal']
# cooper_data = cooper_data[['time', 'Total KW']]
# cooper_data.columns = ['time', 'Utility Subtotal']
cooper_data.time = pd.to_datetime(cooper_data.time)

# join on time
data = pd.merge(cooper_data, weather_data, on=['time'])
# data = data[np.isfinite(data.DB) & np.isfinite(data.WB)]
# data = data.dropna(subset = ['DB', 'WB'])

print(data.head)
# data.to_csv('2016_distboards_weather.csv')