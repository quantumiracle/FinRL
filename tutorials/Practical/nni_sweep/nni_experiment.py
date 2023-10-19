from tutorials.Practical.train_and_test import *
from finrl.config_tickers import *
import time
import nni

test_start_date = '2022-12-1'
test_end_date = '2023-1-1'
# baseline_ticker = 'AXP'  # use first stock in each ticker_list as baseline_ticker

ERL_PARAMS = {
    "learning_rate": 3e-6,
    "batch_size": 2048,
    "gamma": 0.985,
    "seed": 312,
    "net_dimension": 512,
    "target_step": 5000,
    "eval_gap": 30,
    "eval_times": 1,
}

def get_year_month(month_cnt):
    year = month_cnt // 12 + 2019
    month = month_cnt % 12 + 1
    return year, month


def nni_eval(params):
    time_start_month = params.pop("time_start_month")
    time_across_month = params.pop("time_across_month")
    ticker_list = params.pop("ticker_list")
    candle_time_interval = params.pop("candle_time_interval")

    target_step = params.pop("target_step")
    learning_rate = params.pop("learning_rate")
    batch_size = params.pop("batch_size")
    gamma = params.pop("gamma")
    net_dimension = params.pop("net_dimension")

    train_start_date = '{}-{}-1'.format(*get_year_month(time_start_month))
    time_end_month = time_start_month + time_across_month
    time_end_month = min(time_end_month, 35) # within training range
    train_end_date = '{}-{}-1'.format(*get_year_month(time_end_month))

    time_stamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    MODEL_IDX = f'{model_name}_{train_start_date}_{train_end_date}_{time_stamp}'

    ticker_list = eval(ticker_list)

    ERL_PARAMS['target_step'] = target_step
    ERL_PARAMS['learning_rate'] = learning_rate
    ERL_PARAMS['batch_size'] = batch_size
    ERL_PARAMS['gamma'] = gamma
    ERL_PARAMS['net_dimension'] = net_dimension

    value = train_and_test(train_start_date, train_end_date, test_start_date, test_end_date, ticker_list, candle_time_interval,
        ticker_list[0], model_name, MODEL_IDX, to_train=True, erl_params=ERL_PARAMS)
    return value


params = nni.get_next_parameter()

for t in range(1):
    print(f"Epoch {t + 1}\n-------------------------------")
    score: float = nni_eval(params)
    print('score', score)
    # nni.report_intermediate_result(score)  # learning curve
nni.report_final_result(score)

