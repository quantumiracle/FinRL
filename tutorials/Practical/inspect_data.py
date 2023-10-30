import pandas as pd
from datetime import date
from finrl.meta.data_processor import DataProcessor
import os

def clip_by_date(data, start_date, end_date):
    if isinstance(start_date, date):
        start_date = start_date.strftime("%Y-%m-%d")
    if isinstance(end_date, date):
        end_date = end_date.strftime("%Y-%m-%d")

    start_time = pd.Timestamp(start_date + " 00:00:00").tz_localize("America/New_York")
    end_time = pd.Timestamp(end_date + " 23:59:59").tz_localize("America/New_York")
    return data[(start_time <= data['timestamp']) & (data['timestamp'] <= end_time)]


def load_df(start_date, end_date, file_path='./data/DOW30_alpaca_2019-1-1_2023-1-1.pkl'):
    data = pd.read_pickle(file_path)
    data = clip_by_date(data, start_date, end_date)
    return data

### Inspect certain dataset ###

data_path = './data'
data_file_name = ['DOW30_alpaca_2019-1-1_2023-1-1.pkl',
'DOW_30_TICKER_alpaca_2019-1-1_2023-8-31.pkl',
'CHI30_alpaca_2019-1-1_2023-1-1.pkl',
'TECH_20_TICKER_alpaca_2020-1-1_2023-9-30.pkl',
'NAS_100_TICKER_alpaca_2019-1-1_2023-8-31.pkl'
][0]

file_path = os.path.join(data_path, data_file_name)
# data_source = 'alpaca'
# dp = DataProcessor(data_source)

start_date = '2022-12-1'
end_date = '2023-1-1'
data = load_df(start_date, end_date, file_path)
import pdb; pdb.set_trace()