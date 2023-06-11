
# ERL_PARAMS = {,
#     "learning_rate": 3e-6,
#     "batch_size": 2048,
#     "gamma": 0.985,
#     "seed": 312,
#     "net_dimension": 512,
#     "target_step": 5000,
#     "eval_gap": 30
#     "eval_times": 1
# }

search_space = {
    ## Environment Config
    # 'time_start_month': {'_type': 'randint', '_value': [0, 34]},
    # 'time_across_month': {'_type': 'randint', '_value': [1, 12]},
    'time_start_month': {'_type': 'choice', '_value': [0, 6, 12, 24, 30]},
    'time_across_month': {'_type': 'choice', '_value': [1,3,6,12,24]},
    'ticker_list': {'_type': 'choice', '_value': ['DOW_30_TICKER']},
    # 'ticker_list': {'_type': 'choice', '_value': ['DOW_30_TICKER', 'CHINESE_STOCK_TICKER', 'NAS_100_TICKER', 'SP_500_TICKER']},
    'candle_time_interval': {'_type': 'choice', '_value': ['1Min', '5Min', '15Min', '30Min', '60Min']},

    ## Algorithm Config
    # 'target_step': {'_type': 'choice', '_value': [1000, 2000, 5000, 8000]},
    # 'learning_rate': {'_type': 'choice', '_value': [2e-6, 3e-6, 4e-6, 5e-6]},
    # 'batch_size': {'_type': 'choice', '_value': [256, 512, 1024, 2048]},
}