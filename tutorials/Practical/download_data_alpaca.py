from finrl.train import train
from finrl.test import test
from finrl.config_tickers import *
from finrl.config import INDICATORS
from finrl.meta.data_processor import DataProcessor
from private import API_KEY, API_SECRET, API_BASE_URL
import os
import numpy as np
import pandas as pd


# __all__ = ['SINGLE_TICKER', 'CHINESE_STOCK_TICKER', 'DOW_30_TICKER','TECH_20_TICKER', \
#     'NAS_100_TICKER', 'SP_500_TICKER', 'HSI_50_TICKER',\
#     'SSE_50_TICKER', 'CSI_300_TICKER', 'CAC_40_TICKER',\
#     'DAX_30_TICKER',  'TECDAX_TICKER',  'MDAX_50_TICKER',\
#     'SDAX_50_TICKER', 'LQ45_TICKER',  'SRI_KEHATI_TICKER',\
#     'FX_TICKER']
ticker_name = 'TECH_20_TICKER'
ticker_list = eval(ticker_name)

# INDICATORS = [
#     "macd",
#     "boll_ub",
#     "boll_lb",
#     "rsi_30",
#     "cci_30",
#     "dx_30",
#     "close_30_sma",
#     "close_60_sma",
# ]

action_dim = len(ticker_list)
time_interval = '1Min'  # '1Min'

def download_data(
        start_date,
        end_date,
        ticker_list,
        data_source,
        time_interval,
        technical_indicator_list,
        save_path,
        if_vix=True,
        if_train=False,
        **kwargs
):  
        dp = DataProcessor(data_source, **kwargs)
        print('Download data')
        # download data
        data = dp.download_data(ticker_list, start_date, end_date, time_interval)
        data = dp.clean_data(data)
        data = dp.add_technical_indicator(data, technical_indicator_list)
        if if_vix:
            data = dp.add_vix(data)

        # save data
        data.to_pickle(save_path)


# start_date = '2019-1-1'
start_date = '2020-1-1'   # sp

end_date = '2023-9-30'
data_source = 'alpaca'
data_path = 'data'
data_file_name = f'{ticker_name}_{data_source}_{start_date}_{end_date}.pkl'
# data_file_name = f'CHI30_{data_source}_{start_date}_{end_date}.pkl'
save_path = os.path.join(data_path, data_file_name)

if __name__ == "__main__":
        kwargs = {
                'API_KEY': API_KEY,
                'API_SECRET': API_SECRET,
                'API_BASE_URL': API_BASE_URL,

        }
        download_data(start_date, end_date, ticker_list, data_source, time_interval, INDICATORS, save_path, **kwargs)