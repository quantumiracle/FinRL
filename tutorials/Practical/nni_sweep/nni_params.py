
# ERL_PARAMS = {
#     "learning_rate": 3e-6,
#     "batch_size": 2048,
#     "gamma": 0.985,
#     "seed": 312,
#     "net_dimension": 512,
#     "target_step": 5000,
#     "eval_gap": 30,
#     "eval_times": 1,
# }

search_space = {
    ## Environment Config
    # 'time_start_month': {'_type': 'randint', '_value': [12]},
    # 'time_across_month': {'_type': 'randint', '_value': [1, 12]},
    # 'time_start_month': {'_type': 'choice', '_value': [0, 6, 12, 24, 30]},
    # 'time_across_month': {'_type': 'choice', '_value': [1,3,6,12,24]},
    'time_start_month': {'_type': 'choice', '_value': [12]},
    'time_across_month': {'_type': 'choice', '_value': [6]},
    'ticker_list': {'_type': 'choice', '_value': ['DOW_30_TICKER']},
    # 'ticker_list': {'_type': 'choice', '_value': ['DOW_30_TICKER', 'CHINESE_STOCK_TICKER', 'NAS_100_TICKER', 'SP_500_TICKER']},
    # 'candle_time_interval': {'_type': 'choice', '_value': ['1Min', '5Min', '15Min', '30Min', '60Min']},
    'candle_time_interval': {'_type': 'choice', '_value': ['1Min']},

    ## Algorithm Config
    'target_step': {'_type': 'choice', '_value': [2000, 5000, 8000]},
    'learning_rate': {'_type': 'choice', '_value': [1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4]},
    'batch_size': {'_type': 'choice', '_value': [512, 1024, 2048]},
    'gamma': {'_type': 'choice', '_value': [0.985, 0.99, 0.995]},
    'net_dimension': {'_type': 'choice', '_value': [128, 512, 1024]},
}