from nni import Experiment
from nni_sweep.nni_params import *
from datetime import datetime

current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%Y%m%d")
# formatted_date += '_Tech_20'
formatted_date += '_' + '_'.join(search_space['ticker_list']['_value'])  # ticker list names: 'DOW_30_TICKER'


experiment = Experiment('local')
experiment.config.search_space = search_space
experiment.config.trial_command = f'python nni_sweep/nni_experiment.py --date={formatted_date}'
experiment.config.trial_code_directory = '.'
experiment.config.tuner.name = 'TPE'
experiment.config.tuner.class_args['optimize_mode'] = 'maximize'
experiment.config.training_service.use_active_gpu = True
experiment.config.max_trial_number = 10000
experiment.config.trial_concurrency = 20  # number of jobs to run in parallel
# experiment.run(8880)  # start new training
experiment.run(8088)  # start new training

# experiment.resume('vx7qdf8n', 8880)  # resume previous training
# experiment.resume('4u7lxhp1', 8880)  # resume previous training

# experiment.stop()
