import os
import pickle
from typing import Dict

import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import BACKTEST_PARAMS, MODEL_OUTPUT_DIR, BACKTEST_DIR
from src.evaluation.evaluator import Evaluator
# from src.config import FEATURES, FILTERS

class Backtest:
    def __init__(self, 
                 evaluator: Evaluator):
        self.evaluator = evaluator

    def _get_model_info(self, params: dict) -> None:
        """
        Check how many models there are in total, and how many of them are evaluated
        """

        # step 1: get the list of models in MODEL_OUTPUT_DIR
        model_folders = os.listdir(MODEL_OUTPUT_DIR)

        # check for the given set of parameters, how many models are already evaluated
        total_models = len(model_folders)
        backtest_output_dir = self.evaluator.get_backtest_output_dir(BACKTEST_DIR, params)
        if os.path.exists(backtest_output_dir):
            evaluated_model_folders = os.listdir(backtest_output_dir)
            total_evaluated_models = len(evaluated_model_folders)
        else:
            evaluated_model_folders = []
            total_evaluated_models = 0
        # expander_text = f'{total_evaluated_models}/{total_models} ({total_evaluated_models/total_models:.2%}) models backtested'
        expander_text = f'{total_evaluated_models} models backtested'

        # display info
        if total_evaluated_models == total_models:
            expander_text += ' ✅'
        else:
            expander_text += ' 🧐'
        with st.expander(expander_text):
            for i in model_folders:
                if i in evaluated_model_folders:
                    st.markdown(f'- [x] {i}')
                else:
                    st.markdown(f'- [ ] {i}')
        
    def _display_leaderboard(self, df: pd.DataFrame, sort_by: str="cumulative_returns") -> None:
        df2show = df.sort_values(sort_by, ascending=False)
        st.dataframe(
            df2show,
            column_config={
                "model": "Model",
                "return": st.column_config.ProgressColumn(
                                        "Return",
                                        help="Total Amount of Return",
                                        format="%.2f",
                                        min_value=0,
                                        max_value=df2show["return"].max(),
                                    ),
                "cumulative_returns": st.column_config.ProgressColumn(
                                        "Cumulative Return",
                                        help="Total Amount of Cumulative Return",
                                        format="%.2f",
                                        min_value=0,
                                        max_value=df2show["cumulative_returns"].max(),
                                    ),
                "return_line": st.column_config.LineChartColumn(
                    "Return Sparkline",
                    width="medium",
                    help="The return values over the backtested period",
                    y_min=0,
                    # y_max=100,
                ),
                "cumulative_returns_line": st.column_config.LineChartColumn(
                    "Cumulative Return Sparkline",
                    width="medium",
                    help="The cumulative return values over the backtested period",
                    y_min=0,
                    # y_max=100,
                ),
            },
            hide_index=True,
        )

    def _get_leaderboard(self, params: dict) -> None:
        """
        Given the set of backtesting parameters, get the leaderboard data for evaluated models
        """
        backtest_output_dir = self.evaluator.get_backtest_output_dir(BACKTEST_DIR, params)
        if os.path.exists(backtest_output_dir):
            evaluated_model_folders = os.listdir(backtest_output_dir)
            evaluated_model_folders = [i for i in evaluated_model_folders if os.path.isdir(os.path.join(backtest_output_dir, i))]
            # read the pickle file and parse the data for each model, then display it as a dataframe
            model_perf = []
            for model in evaluated_model_folders:
                
                # read the pickle file as a dictionary
                pickle_file = os.path.join(backtest_output_dir, model, 'backtest.pkl')
                with open(pickle_file, 'rb') as handle:
                    b = pickle.load(handle)
                model_perf.append({
                    'model': model,
                    'return': b['returns'][-1],
                    'cumulative_returns': b['cumulative_returns'][-1],
                    'return_line': b['returns'].values,
                    'cumulative_returns_line': b['cumulative_returns'].values,
                })
            df_model_perf = pd.DataFrame(model_perf)
            self._display_leaderboard(df_model_perf)
        else:
            # if there's no evaluated model, we don't show anything
            pass


    def display_backtest(self, params: dict):

        self._get_model_info(params)

        self._get_leaderboard(params)

        # chart = px.line(retention, x='day_to_first_visit',
        #                         y='retention', color='User Type')
        
        # chart.update_layout(
        #     height=300,
        #     margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        #     hovermode='closest',
        #     xaxis_title='Days Since User First Started',
        #     yaxis_title='Percent of Users Retained (%)',
        # )

        # st.plotly_chart(chart, use_container_width=True)