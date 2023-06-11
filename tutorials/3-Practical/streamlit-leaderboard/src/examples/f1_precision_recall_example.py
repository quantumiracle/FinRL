import json
import zipfile
from io import BytesIO
import os

from pathlib import Path
from typing import Tuple, Type, Dict, Optional
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

from src.examples.generate_predictions import GROUND_TRUTH_DATA
from src.evaluation.evaluator import Evaluator
from src.evaluation.metric import Metric
from src.common.utils import files_exist

import sys
sys.path.append(".....")  # root path of Finrl

# all necessary packages for finrl test
from finrl.config import INDICATORS
from finrl.config_tickers import DOW_30_TICKER
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from finrl.plot import backtest_stats, get_daily_return, get_baseline # backtest_plot
from finrl.test import test
from finrl.plot import *
from private import API_KEY, API_SECRET, API_BASE_URL

class F1(Metric):
    @classmethod
    def name(cls) -> str:
        return 'F1'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class CumulativeReturn(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Cumulative Return'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True

class Precision(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Precision'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class Recall(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Recall'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class ExampleEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        self.true_label_dict = GROUND_TRUTH_DATA
        self.labels_array = np.array(list(self.true_label_dict.values()))

    @classmethod
    def metrics(cls) -> Tuple[Type[Metric], ...]:
        return (F1, Precision, Recall)

    def evaluate(self, filepath: Path) -> bool:
        # TODO：
        # 1. check if results are already there
        #   a. if so, read directly the result
        #   b. otherwise, run the test function

        if os.path.exists(filepath.joinpath('backtest.png')):
            print('evaluated already!')
            return True
        else:
            return self._evaluate_backtest(filepath)

    def _evaluate_backtest(self, filepath: Path):
        # TODO：
        # 1. call the test() function here
        # arguments:
        # - start_time
        # - end_time
        # - DOW
        # - ...
        # test(filepath, **conf_json)
        test_start_date = '2022-6-11'
        test_end_date = '2023-1-2'
        baseline_ticker = '^DJI'

        ticker_list = DOW_30_TICKER
        candle_time_interval = '1Min'  # '1Min'
        env = StockTradingEnv

        try:
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
                            # cwd=f'./papertrading_erl/{MODEL_IDX}',  # current_working_dir
                            cwd=filepath,
                            if_plot=True,  # to return a dataframe for backtest_plot
                            break_step=1e7)
            print("============== account_value ===========")
            print(account_value)

            # baseline stats
            print("==============Get Baseline Stats===========")
            # baseline_df_dji = get_baseline(
            #     ticker="^DJI",
            #     start=test_start_date,
            #     end=test_end_date)

            baseline_df = get_baseline(            
                    ticker = baseline_ticker, 
                    start = test_start_date,
                    end = test_end_date)

            stats = backtest_stats(baseline_df, value_col_name='close')
            print(stats)

            print("==============Compare to Baseline===========")
            figs = backtest_plot(account_value, baseline_df)
            figs.savefig(f'{filepath}/backtest.png')
            return True
        except:
            print('error in backtest')
            return False

    def validate_submission(self, io_stream: BytesIO) -> bool:
        io_stream.seek(0)
        try:
            # TODO：
            # 1. check files exist in the zip
            #   a) conf.json
            #   b) process/actor.pth (we might want to extend it to something more general than hardcoded)
            # 2. put it in a temporary folder and run test
            # 3. store the result into a folder for future refrence
            f = zipfile.ZipFile(io_stream)
            required_files = ['conf.json', 'process/actor.pth']
            return files_exist(required_files, f.namelist()) # TODO: return also some information about the missing files            
        except:
            return False