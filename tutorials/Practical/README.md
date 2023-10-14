## Requirements

Python>=3.8 (3.7 will report error for streamlit)

yfinance==0.2.3

pandas==1.5.3

pyfolio needs git clone installation from [source](https://github.com/quantopian/pyfolio), otherwise has error: https://github.com/quantopian/pyfolio/issues/682.

## Usage Instruction

### Alpaca

Train and test using Alpaca data source.

Need to create a `private.py` file under the **root** folder (FinRL) and put your own `API_KEY`, `API_SECRET`, in it in the form of:

```python
API_KEY = you key 
API_SECRET = your secret
API_BASE_URL = 'https://paper-api.alpaca.markets'
```

Run:

```bash
python train_alpaca.py
python test_alpaca.py
python deploy_alpaca.py
```

All-in-one script for train and test:

```
python train_and_test.py
```

### Hyper-parameter Sweep

```
python nni_run.py
# eval all runs
python compare_results.py
```
All sweeping outputs including training configurations and models will be saved to `DATETIME/TrainStamp/` in a format of:
```
conf.json
backtest.pdf
process-
       |-actor.pth
       |-critic.pth
       |-tensorboard
```

### Streamlit On-Page Train/Test/Eval

![streamlit](./img/streamlit.png)

```
streamlit run streamlit_train.py --server.fileWatcherType none
```

**!Note**: A separate subprocess will run for training, need to kill manually with the process ID!

### Streamlit Leaderboard

```
cd streamlit-leaderboard
streamlit run src/app.py
## Or
bash run.sh
```

### Crypto

Crypto trading with Alpaca data.

```
python train_crypto.py
python test_crypto.py
python crypto_trade.py
```

### Notebooks

Under `./notebooks/`

