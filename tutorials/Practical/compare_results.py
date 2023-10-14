import shutil

import numpy as np
import os
import pickle
from finrl.test import test
from finrl.config_tickers import DOW_30_TICKER
from finrl.config import INDICATORS
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from private import API_KEY, API_SECRET, API_BASE_URL

log_path = os.path.join(os.path.dirname(__file__), 'log', )


def _get_full_path(dir_name_list):
    full_path_list = []
    for d in dir_name_list:
        path = os.path.join(log_path, d)
        name_list = os.listdir(path)
        full_path_list.extend([os.path.join(path, name) for name in name_list])
    return full_path_list


def get_top_n_path(dir_name_list, top_n, save_log=True, eval_log_dir=None):
    full_path_list = _get_full_path(dir_name_list)
    num_models = len(full_path_list)
    print("Number of models: ", num_models)
    path2value = {}
    for i, p in enumerate(full_path_list):
        path2value[p] = get_eval_value(p)
        print(f"Progress: {i+1}/{num_models}\n================================")
    result = dict(sorted(path2value.items(), key=lambda x: x[1])[: top_n])
    if save_log:
        with open(os.path.join(eval_log_dir, 'eval_results.pkl'), 'wb') as file:
            pickle.dump(path2value, file)
        with open(os.path.join(eval_log_dir, f'top_{top_n}_results.pkl'), 'wb') as file:
            pickle.dump(result, file)        
    return result
    # return list(result.values())


def filter_ability_path(dir_name_list, v):
    full_path_list = _get_full_path(dir_name_list)
    path2value = {p: get_eval_value(p) for p in full_path_list}
    result = dict(filter(lambda x: x[1] >= v, path2value.items()))
    return result
    # return list(result.values())


# for p in full_path_list:
#     print(p)

def get_eval_value(path):
    file_path = os.path.join(path, 'process', 'recorder.npy')
    if not os.path.isfile(file_path):
        return -np.inf
    # return np.random.random()  # return random value for debug
    # return _get_training_reward(path)  # return value base on last serval training rewards
    return _get_eval_value(path)  # return value base on Real-time test


def _get_training_reward(path):
    file_path = os.path.join(path, 'process', 'recorder.npy')
    # if not os.path.isfile(file_path):
    #     return -np.inf
    data = np.load(file_path)
    """
    steps = recorder[:, 0]  # x-axis is training steps
    r_avg = recorder[:, 1]
    r_std = recorder[:, 2]
    r_exp = recorder[:, 3]
    obj_c = recorder[:, 4]
    obj_a = recorder[:, 5]
    """
    return np.average(data[-10:, 1])  # last 10 times average


def _get_eval_value(path):
    ticker_list = DOW_30_TICKER
    candle_time_interval = '5Min'  # '1Min'

    # MODEL_IDX = f'{model_name}_{start_date}_{end_date}'

    env = StockTradingEnv
    account_value = test(start_date=EVAL_START_DATE,
                         end_date=EVAL_END_DATE,
                         ticker_list=ticker_list,
                         data_source='alpaca',
                         time_interval=candle_time_interval,
                         technical_indicator_list=INDICATORS,
                         drl_lib='elegantrl',
                         env=env,
                         model_name='ppo',
                         API_KEY=API_KEY,
                         API_SECRET=API_SECRET,
                         API_BASE_URL=API_BASE_URL,
                         #       erl_params=ERL_PARAMS,
                         # cwd=f'./papertrading_erl/{MODEL_IDX}',  # current_working_dir
                         cwd=os.path.join(path, 'process/'),  # current_working_dir
                         if_plot=False,  # to return a dataframe for backtest_plot
                         break_step=1e7)
    return account_value[-1] / 100000


if __name__ == "__main__":
    EVAL_START_DATE = '2022-11-1'
    EVAL_END_DATE = '2023-1-1'
    
    eval_log_name = f'eval_{EVAL_START_DATE}_{EVAL_END_DATE}'
    eval_log_dir = f'./log/{eval_log_name}'
    os.makedirs(eval_log_dir, exist_ok=True)

    # dir_list = ['20230924']
    dir_list = ['with_conf']  # run idex under ./log/
    # dir_list = ['ppo_2019-01-01_2023-08-31_2023-9-4-16-45-29']

    # get path result dict
    res = get_top_n_path(dir_list, 5, eval_log_dir=eval_log_dir)
    # res = filter_ability_path(dir_list, 0.8)
    for r in res.items():
        print(r)

    # copy dir to target path
    tar_path = os.path.join(os.path.dirname(__file__), f'/log/selected_with_{eval_log_name}', )
    full_path_list = list(res.keys())
    full_tar_list = [p.replace(log_path, tar_path) for p in full_path_list]

    for path, target in zip(full_path_list, full_tar_list):
        shutil.copytree(path, target)