import streamlit as st
import time
import numpy as np
import sys, pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.evaluation.evaluator import Evaluator
from src.display.backtest import Backtest
from src.backtest.backtest_sidebar import BacktestSidebar
# from src.backtest.backtest_manager import BacktestManager
from src.config import EVALUATOR_CLASS_BACKTEST, EVALUATOR_KWARGS_BACKTEST, MODEL_OUTPUT_DIR, BACKTEST_DIR

@st.cache_data()
def get_backtest_evaluator() -> Evaluator:
    return EVALUATOR_CLASS_BACKTEST(**EVALUATOR_KWARGS_BACKTEST)

# @st.cache_data()
# def get_backtest_manager() -> BacktestManager:
#     return BacktestManager(MODEL_OUTPUT_DIR, BACKTEST_DIR)

@st.cache_data()
def get_backtest_sidebar(username: str) -> BacktestSidebar:
    return BacktestSidebar(
                            username, 
                            # get_backtest_manager(),
                            backtest_validator=get_backtest_evaluator().validate,
                            backtest_evaluator=get_backtest_evaluator().evaluate,
                            #  submission_file_extension=ALLOWED_SUBMISSION_FILE_EXTENSION,
                            )

@st.cache_data()
def get_backtest() -> Backtest:
    return Backtest(get_backtest_evaluator())

st.set_page_config(page_title="Evaluation View", page_icon="📦")

if 'username' not in st.session_state.keys():
    st.session_state['username'] = ''


#=== Sidebar ===#
sidebar = get_backtest_sidebar(st.session_state['username'])

sidebar.run_backtest()

#=== Page ===#

get_backtest().display_backtest(sidebar.get_params())