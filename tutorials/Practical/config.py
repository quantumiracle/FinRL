
InitialCapital = 1e5

ERL_PARAMS = {
    "learning_rate": 3e-6,
    "batch_size": 2048,
    "gamma": 0.985,
    "seed": 312,
    "net_dimension": 512,
    "target_step": 5000,
    "eval_gap": 30,
    "eval_times": 1,
}
# finrl.config.py
RLlib_PARAMS = {"lr": 5e-5, "train_batch_size": 500, "gamma": 0.99}
SAC_PARAMS = {
    "batch_size": 64,
    "buffer_size": 100000,
    "learning_rate": 0.0001,
    "learning_starts": 100,
    "ent_coef": "auto_0.1",
}

SB3_PARAMS = {'n_steps': 2048, 'ent_coef': 0.02, 'learning_rate': 0.0003, 'batch_size': 64}

NNI_TEST_START_DATE = '2022-12-1'
NNI_TEST_END_DATE = '2023-1-1'