from train_and_test import *
import time
import nni

test_start_date = '2022-12-1'
test_end_date = '2023-1-1'
baseline_ticker = 'AXP'


def get_year_month(month_cnt):
    year = month_cnt // 12 + 2019
    month = month_cnt % 12 + 1
    return year, month


def nni_eval(params):
    time_start_month = params.pop("time_start_month")
    train_start_date = '{}-{}-1'.format(*get_year_month(time_start_month))

    time_across_month = time_start_month + params.pop("time_across_month")
    time_across_month = min(time_across_month, 35)
    train_end_date = '{}-{}-1'.format(*get_year_month(time_across_month))

    time_stamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    MODEL_IDX = f'{model_name}_{train_start_date}_{train_end_date}_{time_stamp}'
    value = train_and_test(train_start_date, train_end_date, test_start_date, test_end_date, baseline_ticker,
                           model_name, MODEL_IDX, to_train=True)
    return value


params = nni.get_next_parameter()

for t in range(1):
    print(f"Epoch {t + 1}\n-------------------------------")
    score: float = nni_eval(params)
    print('score', score)
    # nni.report_intermediate_result(score)  # learning curve
nni.report_final_result(score)

