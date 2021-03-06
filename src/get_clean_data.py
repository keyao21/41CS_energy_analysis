import json
from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
import powerdash_info
import requests
import matplotlib.pyplot as plt
import time as ptime

def query_powerdash(start, end, board_name):
    payload = {'start': start, 'end': end, 'dgm': powerdash_info.powerdash_name_to_dgm[board_name],
               'format': 'csv'}
    data = requests.get(url=powerdash_info.powerdash_base_url + "/range", params=payload)
    if data.text == "":
        return None
    return StringIO(data.text)


def get_data(start, end, board_name=None, db=None):
    cache_this = True
    if db is not None:
        data = db.get(board_name)
        if data is not None:
            data = data.decode('ascii')
            data = json.loads(data)
            # deserializeJSON
            if data['start'] <= start and data['end'] >= end:
                csv_data = data['data']
                csv_data = StringIO(csv_data)
                cache_this = False
            else:
                db.delete(board_name)
                csv_data = query_powerdash(start, end, board_name)
        else:
            csv_data = query_powerdash(start, end, board_name)
    else:
        csv_data = query_powerdash(start, end, board_name)

    csv = pd.read_csv(csv_data)
    csv.set_index(pd.DatetimeIndex(csv['time']), inplace=True)
    del csv['time']
    clean_data(csv)
    if board_name == "overall utilities":
        return_data = csv
    else:
        return_data = csv[powerdash_info.powerdash_name_to_series[board_name]]

    if db is not None and cache_this:
        to_cache = cache_data(start, end, board_name, return_data).to_string()
        db.set(board_name, to_cache)

    start = pd.to_datetime(start / 1000, unit='s')
    end = pd.to_datetime(end / 1000, unit='s')

    return return_data[start:end]


def clean_data(data):
    data.fillna(value=0, method=None, inplace=True)


def get_distribution_boards(start, end, db=None):
    data = {}
    for board in powerdash_info.distribution_boards:
        board_data = get_data(start=start, end=end, board_name=board, db=db)
        if board_data is None:
            return None
        data[board] = board_data
    return data


def get_overall(start, end, db=None):
    overall = get_data(start=start, end=end, board_name="overall utilities", db=db)
    if overall is None:
        return None
    data = {}
    return overall
    # let's try getting everything instead
    # data['Utility 1'] = overall['SRV1KW']
    # data['Utility 2'] = overall['SV2KW']
    # return data


def get_recent(hours, board_name):
    start = datetime.now() - timedelta(days=hours)
    end = datetime.now()
    start = int(ptime.mktime(start.timetuple())*1000)
    end = int(ptime.mktime(end.timetuple())*1000)

    # data = get_overall(start, end)
    data = get_distribution_boards(start, end)
    # remove duplicated indexes
    for key, value in data.items():
        data[key] = value[~value.index.duplicated(keep='last')]

    data = pd.DataFrame(data)
    # data = data[board_name]
    # data['minute'] = [ts.minute for ts in data.index]
    # print(data.groupby('minute').mean())
    print( data )
    print( data[board_name] )
    return( data[board_name] )


class cache_data:
    def __init__(self, start, end, board_name, data):
        self.start = start
        self.end = end
        self.data = data
        self.board_name = board_name

    def to_string(self):
        data = self.data.to_csv(header=True, index_label='time')
        to_cache = {'start': self.start, 'end': self.end, 'data': data}
        return json.dumps(to_cache, ensure_ascii=True)


if __name__ == "__main__":
    # start = 1483241304000 # 1/1/17
    # end   = 1509561781000 # 11/1/17
    # start = 1451606400000 # 1/1/2016
    # end = 1483228799000 # 12/31/2016

    # start = 1420074061000 #1/1/2015
    start = 1451610061000 #1/1/2016
    # start = '1/31/2018'
    
    # board_name = 'roof mechanical'
    # get_recent(hours=1, board_name=board_name)

    # start = datetime.now() - timedelta(days=1)
    end = datetime.now()
    # start = int(ptime.mktime(start.timetuple())*1000)
    end = int(ptime.mktime(end.timetuple())*1000)

    data = get_overall(start, end)
    # data = get_distribution_boards(start, end)
    # remove duplicated indexes
    for key, value in data.items():
        data[key] = value[~value.index.duplicated(keep='last')]

    data = pd.DataFrame(data)
    # print( data['roof mechanical'].head() )
    
    print (data.head())
    data.to_csv('../data/all_data.csv')


    # data = get_distribution_boards(start=start, end=end)
    # data = pd.DataFrame(data)
    # print (data.head())
    # data.to_csv('distribution_board_data/archive/2017.csv')
    # plt.figure()
    # data.plot()
    # plt.savefig('distribution_bds.pdf', format='pdf')
    # plt.show()





