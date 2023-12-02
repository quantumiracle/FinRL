from tutorials.Practical.train_and_test import *
from tutorials.Practical.config import ERL_PARAMS, NNI_TEST_START_DATE, NNI_TEST_END_DATE
from finrl.config_tickers import *
import time
import nni
import argparse
import random

def get_year_month(month_cnt):
    year = month_cnt // 12 + 2019
    month = month_cnt % 12 + 1
    return year, month

def overwrite_params(default_dict, update_dict):
    # overwrite the value in default_dict with update_dict if key exists in default_dict
    default_dict = default_dict.copy()
    for key in update_dict.keys():
        if key in default_dict.keys():
            default_dict[key] = update_dict[key]
    return default_dict

def nni_eval(params):
    time_start_month = params.pop("time_start_month")
    time_across_month = params.pop("time_across_month")
    ticker_list_name = params.pop("ticker_list")
    num_stocks = params.pop("num_stocks", int(1e5))  # by default use all stocks in list
    candle_time_interval = params.pop("candle_time_interval")
    break_step = params.pop("break_step", int(1e7))
    model_name = params.pop("model_name", 'ppo')
    alg_lib = params.pop("alg_lib", 'elegantrl')
    
    train_start_date = '{}-{}-1'.format(*get_year_month(time_start_month))
    time_end_month = time_start_month + time_across_month
    time_end_month = min(time_end_month, 35) # within training range
    train_end_date = '{}-{}-1'.format(*get_year_month(time_end_month))

    time_stamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    # Generate a random 5-digit integer
    random_number = random.randint(10000, 99999)
    model_idx = f'{model_name}_{train_start_date}_{train_end_date}_{time_stamp}_{random_number}'

    ticker_list = eval(ticker_list_name)[:num_stocks]
    baseline_ticker = ticker_list[0]

    rl_params = overwrite_params(ERL_PARAMS, params)

    value = train_and_test(train_start_date, train_end_date, NNI_TEST_START_DATE, NNI_TEST_END_DATE, ticker_list_name, ticker_list, candle_time_interval,
        baseline_ticker, model_name, model_idx, break_step=break_step, to_train=True, alg_lib=alg_lib, rl_params=rl_params, date_prefix=args.date)
    return value

parser = argparse.ArgumentParser(description="Launch configurations.")

# add arguments
parser.add_argument("--date", type=str, default='', help="An argument which takes a value from a set of choices")
args = parser.parse_args()

params = nni.get_next_parameter()

for t in range(1):
    print(f"Epoch {t + 1}\n-------------------------------")
    score: float = nni_eval(params)
    print('score', score)
    # nni.report_intermediate_result(score)  # learning curve
nni.report_final_result(score)  # default metric

