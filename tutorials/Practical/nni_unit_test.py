from nni import Experiment
from nni_sweep.nni_params import *
from datetime import datetime

current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%Y%m%d")
formatted_date += 'test'

search_space = {
    ## Environment Config
    'time_start_month': {'_type': 'choice', '_value': [12]},
    'time_across_month': {'_type': 'choice', '_value': [12]},  # 12
    # 'ticker_list': {'_type': 'choice', '_value': ['DOW_30_TICKER']},
    'ticker_list': {'_type': 'choice', '_value': ['TECH_20_TICKER']},
    'candle_time_interval': {'_type': 'choice', '_value': ['1Min',]},

    ## Algorithm Config
    'target_step': {'_type': 'choice', '_value': [2000,]},
    'learning_rate': {'_type': 'choice', '_value': [1e-4, ]},
    'batch_size': {'_type': 'choice', '_value': [2048]},
    'gamma': {'_type': 'choice', '_value': [0.995]},
    'net_dimension': {'_type': 'choice', '_value': [128]},
    'break_step': {'_type': 'choice', '_value': [100]},  # default 1e7, smaller for test
}

experiment = Experiment('local')
experiment.config.search_space = search_space
experiment.config.trial_command = f'python nni_sweep/nni_experiment.py --date={formatted_date}'
experiment.config.trial_code_directory = '.'
experiment.config.tuner.name = 'TPE'
experiment.config.tuner.class_args['optimize_mode'] = 'maximize'
experiment.config.training_service.use_active_gpu = True
experiment.config.max_trial_number = 10000
experiment.config.trial_concurrency = 1  # number of jobs to run in parallel
# experiment.run(8880)  # start new training
experiment.run(8088)  # start new training

# experiment.stop()
