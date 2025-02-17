from typing import Optional, Callable, Dict
from pathlib import Path

import streamlit as st
import os
import time

from src.config import ADMIN_USERNAME, BACKTEST_PARAMS, MODEL_OUTPUT_DIR, BACKTEST_DIR
from src.common.utils import loadImg

class BacktestSidebar:
    def __init__(self, username: str, 
                # backtest_manager: BacktestManager,
                 backtest_validator: Optional[Callable[[Path], bool]] = None,
                 backtest_evaluator: Optional[Callable[[Path, Path, Dict], bool]] = None,
                 ):
        self.username = username
        self.backtest_validator = backtest_validator
        self.backtest_evaluator = backtest_evaluator
        self.file_uploader_key = f"file upload {username}"
        
        # paramters for backtesting
        self._params = {}

    def __init_counters(self):
        '''
        @brief: count how many models are evaluated, successfully or not 
        '''
        self._backtest_return_code = {
            0: 0, # evaluation existed
            1: 0, # new evaluation succeeded
            2: 0, # new evaluation failed
        }
        
    def get_params(self):
        return self._params.copy()

    def run_backtest(self):
        st.markdown(f"# Backtest (Dev)")

        st.sidebar.title(f"Hello {self.username}!")
        
        if self.username != ADMIN_USERNAME:
            st.sidebar.markdown("## Backtest Your Models :fire:")

            #--- select backtesting configurations
            for k, v in BACKTEST_PARAMS.items():
                self._params[k] = v[0](v[1], v[2]) # streamlit_element(prompt, default_value/options)

            # test arguments
            # test 1: start_date < end_date
            if self._params['start_date'] >= self._params['end_date']:
                st.sidebar.error('Please make sure that start date < end date.')
            self._backtest()
        


    def _backtest(self):
        # backtest return counter
        self.__init_counters()

        # step 1: get the list of models in MODEL_OUTPUT_DIR
        model_folders = os.listdir(MODEL_OUTPUT_DIR)
        
        # Folder selection with an 'All' option
        all_folders = model_folders
        selected_folders = st.multiselect("Select folders", ["All"] + all_folders, default=["All"])

        # If 'All' is selected, use all folders
        if "All" in selected_folders:
            selected_folders = all_folders

        total_models_to_backtest = 0
        for folder in selected_folders:
            if os.path.isdir(os.path.join(MODEL_OUTPUT_DIR, folder)):
                total_models_to_backtest += len(os.listdir(os.path.join(MODEL_OUTPUT_DIR, folder)))

        if st.sidebar.button('Backtest'):
            progress_value = 0
            with st.spinner('Wait for it...'):
                progress_text = f"{total_models_to_backtest} models to backtest, please wait..."
                progress_bar = st.sidebar.progress(0, text=progress_text)
                for j, folder in enumerate(selected_folders):
                    # emumerate all model folders under selected_folders
                    for i, file in enumerate(os.listdir(os.path.join(MODEL_OUTPUT_DIR, folder))):
                        model_path = os.path.join(MODEL_OUTPUT_DIR, folder, file)
                        print(model_path)
                        # first check if the folder is valid
                        if self.backtest_validator(model_path):
                            backtest_res = self.backtest_evaluator(model_path, BACKTEST_DIR, self._params)
                            self._backtest_return_code[backtest_res] += 1
                            progress_value = (i + 1)/total_models_to_backtest
                            progress_bar.progress(progress_value, text=progress_text)
                        else:
                            print(f'Error: invalid model {model_path}')
            progress_bar.progress(progress_value, text=f"{total_models_to_backtest} backtest done!")
            st.success('Backtest Done!')
            if self._backtest_return_code[2] > 0:
                st.error(f'{self._backtest_return_code[2]} models failed evaluation', icon="🚨")

            # step 2: check if the directory for each model exists


            return
