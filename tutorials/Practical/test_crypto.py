import sys
sys.path.append('/home/quantumiracle/research/FinRL-Meta')
from finrl.meta.env_cryptocurrency_trading.env_multiple_crypto import CryptoEnv
from finrl.test import test

# import DRL agents
# from agents.stablebaselines3_models import DRLAgent as DRLAgent_sb3
# from agents.rllib_models import DRLAgent as DRLAgent_rllib
# from agents.elegantrl_models import DRLAgent as DRLAgent_erl

# import data processor
from finrl.meta.data_processor import DataProcessor
from private import API_KEY, API_SECRET, API_BASE_URL
import numpy as np
import pandas as pd

TICKER_LIST = ['BTCUSDT','ETHUSDT','ADAUSDT','BNBUSDT','XRPUSDT',
                'SOLUSDT','DOTUSDT', 'DOGEUSDT','AVAXUSDT','UNIUSDT']

env = CryptoEnv
TRAIN_START_DATE = '2021-09-01'
TRAIN_END_DATE = '2021-09-02'

TEST_START_DATE = '2021-01-01'
TEST_END_DATE = '2021-02-01'

INDICATORS = ['macd', 'rsi', 'cci', 'dx'] #self-defined technical indicator list is NOT supported yet

ERL_PARAMS = {"learning_rate": 2**-15,"batch_size": 2**11,
                "gamma": 0.99, "seed":312,"net_dimension": 2**9, 
                "target_step": 5000, "eval_gap": 30, "eval_times": 1}

account_value_erl = test(start_date = TEST_START_DATE, 
                        end_date = TEST_END_DATE,
                        ticker_list = TICKER_LIST, 
                        data_source = 'alpaca-crypto',
                        time_interval= '60Min', 
                        technical_indicator_list= INDICATORS,
                        drl_lib='elegantrl', 
                        env=env, 
                        model_name='ppo', 
                        API_KEY = API_KEY, 
                        API_SECRET = API_SECRET, 
                        API_BASE_URL = API_BASE_URL,
                        current_working_dir='./test_ppo', 
                        net_dimension = 2**9, 
                        if_vix=False
                        )

# plotting
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
#calculate agent returns
account_value_erl = np.array(account_value_erl)
agent_returns = account_value_erl/account_value_erl[0]
#calculate buy-and-hold btc returns
price_array = np.load('./price_array.npy')
btc_prices = price_array[:,0]
buy_hold_btc_returns = btc_prices/btc_prices[0]
#calculate equal weight portfolio returns
price_array = np.load('./price_array.npy')
initial_prices = price_array[0,:]
equal_weight = np.array([1e5/initial_prices[i] for i in range(len(TICKER_LIST))])
equal_weight_values = []
for i in range(0, price_array.shape[0]):
    equal_weight_values.append(np.sum(equal_weight * price_array[i]))
equal_weight_values = np.array(equal_weight_values)
equal_returns = equal_weight_values/equal_weight_values[0]
#plot 
plt.figure(dpi=200)
plt.grid()
plt.grid(which='minor', axis='y')
plt.title('Cryptocurrency Trading ', fontsize=20)
plt.plot(agent_returns, label='ElegantRL Agent', color = 'red')
plt.plot(buy_hold_btc_returns, label='Buy-and-Hold BTC', color='blue')
plt.plot(equal_returns, label='Equal Weight Portfolio', color='green')
plt.ylabel('Return', fontsize=16)
plt.xlabel('Times (5min)', fontsize=16)
plt.xticks(size=14)
plt.yticks(size=14)
'''ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(210))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(21))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.005))
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=2))
ax.xaxis.set_major_formatter(ticker.FixedFormatter([]))'''
plt.legend(fontsize=10.5)
plt.show()