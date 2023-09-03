from typing import Dict

import streamlit as st
import pandas as pd
import plotly.express as px

from src.evaluation.evaluator import Evaluator
# from src.config import FEATURES, FILTERS

class Backtest:
    def __init__(self, 
                 evaluator: Evaluator):
        self.evaluator = evaluator

    def _get_backtest(self, feature: str, filter: dict) -> pd.DataFrame:
        # metric_names = [metric.name() for metric in self.evaluator.metrics()]

        retention = self.evaluator.evaluate(feature, filter)

        return retention

    def display_backtest(self, params: dict):

        st.markdown(f"# Backtest (Dev)")

        st.markdown(f"## Configuration")
        for k, v in params.items():
            st.markdown(f"`{k}: {v}`")

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