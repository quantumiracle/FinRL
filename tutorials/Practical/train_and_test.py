from finrl.train import train, load_df
from finrl.test import test
from finrl.config_tickers import *
from finrl.config import INDICATORS
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from finrl.plot import backtest_stats, backtest_plot, get_baseline, backtest_plot_v2, get_baseline_v2 # backtest_plot
from private import API_KEY, API_SECRET, API_BASE_URL
import os, json
from datetime import datetime

StockPool = 'DOW_30_TICKER'
NumStock = 30
ticker_list = eval(StockPool)[: int(NumStock)]
# ticker_list = CHINESE_STOCK_TICKER[:30]
AlgoLib = ['elegantrl', 'rllib', 'stable_baselines3'][0]

action_dim = len(ticker_list)
candle_time_interval = '1Min'  # '1Min'

env = StockTradingEnv

ERL_PARAMS = {"learning_rate": 3e-6, "batch_size": 2048, "gamma": 0.985,
              "seed": 312, "net_dimension": 512, "target_step": 5000, "eval_gap": 30,
              "eval_times": 1}
# train_start_date = '2019-1-1'
# train_end_date = '2023-1-1'
train_start_date = '2022-6-11'
train_end_date = '2022-8-11'

test_start_date = '2022-6-11'
test_end_date = '2022-9-2'
baseline_ticker = 'AXP'

model_name = 'ppo'
MODEL_IDX = f'{model_name}_{train_start_date}_{train_end_date}'
MODEL_IDX = 'ppo_2022-6-11_2022-8-11_2023-3-4-0-10-6'


def train_and_test(
        train_start_date,
        train_end_date,
        test_start_date,
        test_end_date,
        ticker_list,
        candle_time_interval,
        baseline_ticker,
        model_name,
        MODEL_IDX,
        to_train=False,
        erl_params=None,
):  
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y%m%d")
    os.makedirs(f'./log/{formatted_date}', exist_ok=True)
    save_path = f'./log/{formatted_date}/{MODEL_IDX}'
    os.makedirs(save_path, exist_ok=True)

    if to_train:
        if erl_params is None:
            curr_params = ERL_PARAMS
        else:
            curr_params = erl_params
        log_dict = {}

        training_args = {
            "start_date": train_start_date,
            "end_date": train_end_date,
            "ticker_list": ticker_list,
            "data_source": "alpaca",
            "time_interval": candle_time_interval,
            "technical_indicator_list": INDICATORS,
            "drl_lib": AlgoLib,
            "env": env,
            "model_name": model_name,
            "API_KEY": API_KEY,
            "API_SECRET": API_SECRET,
            "API_BASE_URL": API_BASE_URL,
            "erl_params": curr_params,
            "cwd": os.path.join(save_path, "process/"),  # current_working_dir
            "wandb": False,  # wand be cannot be run in a subprocess
            "break_step": 1e7,
        }

        # logging above info
        log_dict["StockPool"] = StockPool
        log_dict["NumStock"] = NumStock
        log_dict["TickerList"] = training_args["ticker_list"]
        log_dict["DataSource"] = training_args["data_source"]
        log_dict["IndicatorList"] = training_args["technical_indicator_list"]
        log_dict["Algo"] = model_name
        log_dict["AlgoLib"] = AlgoLib
        log_dict["TrainStartDate"] = train_start_date
        log_dict["TrainEndDate"] = train_end_date
        log_dict["TrainTradeInterval"] = candle_time_interval
        log_dict["ErlParams"] = curr_params
        log_dict["BreakStep"] = training_args["break_step"]

        if not os.path.exists(save_path):
            os.mkdir(save_path)
        save_file = open(os.path.join(save_path, "conf.json"), "w")
        json.dump(log_dict, save_file)
        save_file.close()

        train(**training_args)

        # train(start_date=train_start_date,
        #     end_date=train_end_date,
        #     ticker_list=ticker_list,
        #     data_source='alpaca',
        #     time_interval=candle_time_interval,
        #     technical_indicator_list=INDICATORS,
        #     drl_lib='elegantrl',
        #     #       drl_lib='rllib',
        #     #       drl_lib='stable_baselines3',
        #     env=env,
        #     model_name=model_name,
        #     API_KEY=API_KEY,
        #     API_SECRET=API_SECRET,
        #     API_BASE_URL=API_BASE_URL,
        #     erl_params=curr_params,
        #     cwd=f'./log/{MODEL_IDX}',  # current_working_dir
        #     wandb=False,
        #     break_step=1e7)

    account_value = test(start_date=test_start_date,
                         end_date=test_end_date,
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
                         cwd=f'./log/{MODEL_IDX}',  # current_working_dir
                         if_plot=True,  # to return a dataframe for backtest_plot
                         break_step=1e7)
    print("============== account_value ===========")
    print(account_value)

    # baseline stats
    print("==============Get Baseline Stats===========")
    baseline_df = get_baseline_v2(            
            ticker = baseline_ticker, 
            start = test_start_date,
            end = test_end_date)

    stats = backtest_stats(baseline_df, value_col_name='close')
    print(stats)

    print("==============Compare to Baseline===========")
    figs, returns = backtest_plot_v2(account_value, baseline_df)
    figs.savefig(f'./log/{formatted_date}/{MODEL_IDX}/backtest.pdf')
    # return returns.sum()
    if isinstance(account_value, list): # if_plot = False
        return account_value[-1]
    else:
        return account_value['account_value'].iloc[-1]



if __name__ == '__main__':  
    value = train_and_test(train_start_date, train_end_date, test_start_date, test_end_date, ticker_list, candle_time_interval, 
    baseline_ticker, model_name, MODEL_IDX, )
    print('final value: ', value)
