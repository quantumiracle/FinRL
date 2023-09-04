from pathlib import Path
import streamlit as st
import datetime
from src.examples.backtest_evaluation import BacktestEvaluator
from finrl.config_tickers import DOW_30_TICKER

# DOW_30_TICKER = [
#     "AXP",
#     "AMGN",
#     "AAPL",
#     "BA",
#     "CAT",
#     "CSCO",
#     "CVX",
#     "GS",
#     "HD",
#     "HON",
#     "IBM",
#     "INTC",
#     "JNJ",
#     "KO",
#     "JPM",
#     "MCD",
#     "MMM",
#     "MRK",
#     "MSFT",
#     "NKE",
#     "PG",
#     "TRV",
#     "UNH",
#     "CRM",
#     "VZ",
#     "V",
#     "WBA",
#     "WMT",
#     "DIS",
#     "DOW",
# ]

# The class used for the evaluation of the users' submissions.
EVALUATOR_CLASS = BacktestEvaluator
EVALUATOR_KWARGS = {}

# The directory in which the users' submissions will be saved
SUBMISSIONS_DIR = Path(__file__).parent.parent.absolute() / 'user_submissions'

# The name of the encrypted passwords file
PASSWORDS_DB_FILE = Path(__file__).parent.parent.absolute() / 'passwords.db'
ARGON2_KWARGS = {}

# Maximum number of users allowed in the system. If None, no limitation is enforced.
MAX_NUM_USERS = None

# The extension type required for a submission file (e.g. ".json"). If None, any extension is allowed.
ALLOWED_SUBMISSION_FILE_EXTENSION = 'zip'

SHOW_TOP_K_ONLY = 5

ADMIN_USERNAME = 'admin'

ALLOW_FIRST_LOGIN = False

DEV_MODE = True

#--- for backtesting
'''
=== BACKTESTING ===
@brief: 
- take models from $MODEL_OUTPUT_DIR
- select configurations 
store the evaluation results
'''

EVALUATOR_CLASS_BACKTEST = BacktestEvaluator
EVALUATOR_KWARGS_BACKTEST = {}

# The directory in which the trained models are dumped
MODEL_OUTPUT_DIR = Path(__file__).parent.parent.absolute() / 'model_output'
# The directory in which the evaluation results are dumped
BACKTEST_DIR = Path(__file__).parent.parent.absolute() / 'backtest_output'

'''
- src
- model_output
    - ppo_2023-xxx_2023_xxx
    - ppo_2023-xxx_2023_xxx
    - ppo_2023-xxx_2023_xxx
    - trpo_2023
- backtest_output
    - start_date=2023-07-11
        - end_date=xxx
            - ...
                -
                    - ppo_2023-xxx_2023_xxx
                        - xxx.pdf
                        - ...
                        - result.csv
                    - ppo_2023-xxx_2023_xxx
                    - ppo_2023-xxx_2023_xxx
                    - trpo_2023
'''

BACKTEST_VERSION = 'v0'

BACKTEST_PARAMS = {
    'start_date': [
        st.sidebar.date_input, # streamlit element
        "Input the test start date", # prompt
        datetime.date(2022, 6, 11), # default date
    ],
    'end_date': [
        st.sidebar.date_input, # streamlit element
        "Input the test end date", # prompt
        datetime.date(2022, 11, 30), # default date
    ],
    'baseline_ticker': [
        st.sidebar.selectbox, # streamlit element
        "Select the baseline ticker that you want to compare!", # prompt
        DOW_30_TICKER, # list to select
    ],
    'ticker_list': [
        st.sidebar.selectbox, # streamlit element
        "Select the list of tickers for the model", # prompt
        ['DOW_30_TICKER'], # for now only support the DOW_30
    ],
    'candle_time_interval': [
        st.sidebar.selectbox, # streamlit element
        "Select the trading interval", # prompt
        ['1Min', '5Min', '10Min', '15Min', '30Min', '60Min']
    ],
}

BACKTEST_MAX_WORKER = 48
