from finrl.train import train, load_df
from finrl.test import test
from finrl.config_tickers import *
from finrl.config import INDICATORS
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from finrl.plot import backtest_stats, backtest_plot, get_baseline, backtest_plot_v2, get_baseline_v2 # backtest_plot
from private import API_KEY, API_SECRET, API_BASE_URL
import os, json
from datetime import datetime
from tutorials.Practical.config import ERL_PARAMS, AlgoLib, InitialCapital


def train_and_test(
        train_start_date,
        train_end_date,
        test_start_date,
        test_end_date,
        ticker_list_name='',
        ticker_list=[],
        candle_time_interval='1Min',
        baseline_ticker='',
        model_name='',
        model_idx='',
        env = StockTradingEnv,
        break_step=1e7,
        to_train=False,
        erl_params=None,
        date_prefix=None,
):  
    if date_prefix is None:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y%m%d")
    else:
        formatted_date = date_prefix
    os.makedirs(f'./log/{formatted_date}', exist_ok=True)
    save_path = f'./log/{formatted_date}/{model_idx}'
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
            "ticker_list_name": ticker_list_name,
            "ticker_list": ticker_list,
            "data_source": "alpaca",
            "time_interval": candle_time_interval,
            "technical_indicator_list": INDICATORS,
            "drl_lib": AlgoLib,
            "env": env,
            "initial_capital": InitialCapital,
            "model_name": model_name,
            "API_KEY": API_KEY,
            "API_SECRET": API_SECRET,
            "API_BASE_URL": API_BASE_URL,
            "erl_params": curr_params,
            "cwd": os.path.join(save_path, "process/"),  # current_working_dir
            "wandb": False,  # wand be cannot be run in a subprocess
            "break_step": break_step,
        }

        # logging above info
        log_dict["StockPool"] = ticker_list_name
        log_dict["NumStock"] = len(ticker_list)
        log_dict["IniCapital"] = training_args['initial_capital']
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

    account_value, log = test(start_date=test_start_date,
                         end_date=test_end_date,
                         ticker_list_name=ticker_list_name,
                         ticker_list=ticker_list,
                         data_source='alpaca',
                         time_interval=candle_time_interval,
                         technical_indicator_list=INDICATORS,
                         drl_lib=AlgoLib,
                         env=env,
                         initial_capital=InitialCapital,
                         model_name='ppo',
                         API_KEY=API_KEY,
                         API_SECRET=API_SECRET,
                         API_BASE_URL=API_BASE_URL,
                         #       erl_params=ERL_PARAMS,
                         cwd=os.path.join(save_path, "process/"),  # current_working_dir
                         if_plot=True,  # to return a dataframe for backtest_plot
                         return_log=False,  # still return a log placeholder
                         break_step=break_step)
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
    figs.savefig(os.path.join(save_path, "backtest.pdf"))
    # return returns.sum()
    if isinstance(account_value, list): # if_plot = False
        return account_value[-1] / InitialCapital
    else:
        return account_value['account_value'].iloc[-1] / InitialCapital



if __name__ == '__main__':  
    StockPool = 'DOW_30_TICKER'
    NumStock = 30
    ticker_list = eval(StockPool)[: int(NumStock)]
    # ticker_list = CHINESE_STOCK_TICKER[:30]

    action_dim = len(ticker_list)
    candle_time_interval = '1Min'  # '1Min'

    # train_start_date = '2019-1-1'
    # train_end_date = '2023-1-1'
    train_start_date = '2022-6-11'
    train_end_date = '2022-8-11'

    test_start_date = '2022-6-11'
    test_end_date = '2022-9-2'
    baseline_ticker = 'AXP'

    model_name = 'ppo'
    model_idx = f'{model_name}_{train_start_date}_{train_end_date}'
    model_idx = 'ppo_2022-6-11_2022-8-11_2023-3-4-0-10-6'

    value = train_and_test(train_start_date, train_end_date, test_start_date, test_end_date, StockPool, ticker_list, candle_time_interval, 
    baseline_ticker, model_name, model_idx, )
    print('final value: ', value)
