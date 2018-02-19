import pandas as pd

# data source : ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/

def weatherData(year):
    weather_data = pd.read_csv('weather_data/{}.csv'.format(year), 
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



weatherData(2015).to_csv('weather_data/New_York_Hourly_2015.csv')


