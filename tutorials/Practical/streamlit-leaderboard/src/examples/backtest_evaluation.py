import json
import zipfile
from io import BytesIO
import os

from pathlib import Path
from typing import Tuple, Type, Dict, Optional
import numpy as np

from src.evaluation.evaluator import Evaluator
from src.evaluation.metric import Metric
from src.common.utils import files_exist, backtest_plot

import sys
sys.path.append("../..")

# all necessary packages for finrl test
from finrl.config import INDICATORS
from finrl.config_tickers import DOW_30_TICKER
from finrl.meta.env_stock_trading.env_stocktrading_np import StockTradingEnv
from finrl.plot import backtest_stats, get_daily_return, get_baseline # backtest_plot
from finrl.test import test
from finrl.plot import *
from private import API_KEY, API_SECRET, API_BASE_URL

class CumulativeReturn(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Cumulative Return'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class BacktestEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        # self.labels_array = np.array(list(self.true_label_dict.values()))

    @classmethod
    def metrics(cls) -> Tuple[Type[Metric], ...]:
        return (CumulativeReturn)

    def get_backtest_output_dir(self, output_path: Path, params: Dict) -> str:
        res = output_path
        for k, v in params.items():
            res = os.path.join(res, f'{k}={v}')
        return res

    def validate(self, model_path: Path) -> bool:
        res = True
        # test 1: it should be a folder
        res &= os.path.isdir(model_path)
        # test 2: it should contain conf.json
        res &= os.path.exists(os.path.join(model_path, 'conf.json'))
        if not os.path.exists(os.path.join(model_path, 'conf.json')):
            print(f'conf.json not exists in path: {model_path}')
        # test 3: it should contain actor.pth
        res &= os.path.exists(os.path.join(model_path, 'process', 'actor.pth'))
        if not os.path.exists(os.path.join(model_path, 'process', 'actor.pth')):
            print(f'actor.pth not exists in path: {model_path}/process')
        # # test 3: it should contain actor.pth
        # res &= os.path.exists(os.path.join(model_path, 'actor.pth'))
        return res

    def evaluate(self, model_path: Path, output_path: Path, params: Dict) -> int:
        '''
        @brief: check if results are already there
            a. if so, read directly the result
            b. otherwise, run the test function
        @return:
            0 - evaluated already
            1 - evaluation succeeded
            2 - evaluation failed
        '''
        if os.path.exists(os.path.join(self.get_backtest_output_dir(output_path, params), 'backtest.png')):
            print('evaluated already!')
            return 0
        else:
            return self._evaluate_backtest(model_path, output_path, params)

    def _evaluate_backtest(self, model_path: Path, output_path: Path, params: Dict) -> int:
        env = StockTradingEnv

        # try:
        account_value = test(
            start_date=params['start_date'].strftime("%Y-%m-%d"),
            end_date=params['end_date'].strftime("%Y-%m-%d"),
            ticker_list=params['ticker_list'],
            data_source='alpaca',
            time_interval=params['candle_time_interval'],
            technical_indicator_list=INDICATORS,
            drl_lib='elegantrl',
            env=env,
            model_name='ppo',
            API_KEY=API_KEY,
            API_SECRET=API_SECRET,
            API_BASE_URL=API_BASE_URL,
            cwd=os.path.join(model_path, "process/"),
            if_plot=True,  # to return a dataframe for backtest_plot
            break_step=1e7)
        print("============== account_value ===========")
        print(account_value)

        # baseline stats
        print("==============Get Baseline Stats===========")
        baseline_df = get_baseline_v2(            
                ticker = params['baseline_ticker'], 
                start = params['start_date'].strftime("%Y-%m-%d"),
                end = params['end_date'].strftime("%Y-%m-%d")
        )

        stats = backtest_stats(baseline_df, value_col_name='close')
        print(stats)

        print("==============Compare to Baseline===========")
        figs, returns = backtest_plot_v2(account_value, baseline_df)
        os.makedirs(f'{self.get_backtest_output_dir(output_path, params)}', exist_ok=True)
        figs.savefig(f'{self.get_backtest_output_dir(output_path, params)}/backtest.png')
        return 1
        # except:
        #     print('!!! error in backtest !!!')
        #     return 2

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
