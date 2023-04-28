import json
import zipfile
from io import BytesIO
import os

from pathlib import Path
from typing import Tuple, Type, Dict, Optional
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

from src.examples.generate_predictions import GROUND_TRUTH_DATA
from src.evaluation.evaluator import Evaluator
from src.evaluation.metric import Metric
from src.common.utils import files_exist

class F1(Metric):
    @classmethod
    def name(cls) -> str:
        return 'F1'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class Precision(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Precision'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class Recall(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Recall'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True


class ExampleEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        self.true_label_dict = GROUND_TRUTH_DATA
        self.labels_array = np.array(list(self.true_label_dict.values()))

    @classmethod
    def metrics(cls) -> Tuple[Type[Metric], ...]:
        return (F1, Precision, Recall)

    def evaluate(self, filepath: Path) -> bool:
        # TODO：
        # 1. check if results are already there
        #   a. if so, read directly the result
        #   b. otherwise, run the test function

        if os.path.exists(filepath.joinpath('backtest.png')):
            print('evaluated already!')
            return True
        else:
            return self._evaluate_backtest(filepath)

    def _evaluate_backtest(self, filepath: Path):
        # TODO：
        # 1. call the test() function here
        print("TBD")
        pass

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