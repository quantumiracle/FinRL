import json
from pathlib import Path
from PIL import Image
import logging
import pandas as pd
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

def remove_illegal_filename_characters(input_string: str) -> str:
    return "".join(x if (x.isalnum() or x in "._- ") else '_' for x in input_string).strip()


def is_legal_filename(filename: str) -> bool:
    return remove_illegal_filename_characters(filename) == filename

# ---
# Logging 

def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_ip = get_remote_ip()
        return super().filter(record)

def init_logging():
    # Make sure to instanciate the logger only once
    # otherwise, it will create a StreamHandler at every run
    # and duplicate the messages

    # create a custom logger
    logger = logging.getLogger("foobar")
    if logger.handlers:  # logger is already setup, don't setup again
        return
    logger.propagate = False
    logger.setLevel(logging.INFO)
    # in the formatter, use the variable "user_ip"
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s [user_ip=%(user_ip)s] - %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.addFilter(ContextFilter())
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ---
# This set of functions allows to show no pages before login

def get_all_pages(default_page: str) -> dict:
    default_pages = get_pages(default_page)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page(default_page: str):
    current_pages = get_pages(default_page)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages(default_page)

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()

def show_all_pages(default_page: str):
    current_pages = get_pages(default_page)

    saved_pages = get_all_pages(default_page)

    missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

    # Replace all the missing pages
    for key in missing_keys:
        current_pages[key] = saved_pages[key]

    _on_pages_changed.send()


# ---
# utility functions

def files_exist(files: list(), list2check: list()):
    # cleanup the list of files
    list2check = [l for l in list2check if ('__MACOSX' not in l)]

    for f in files:
        matching = [s for s in list2check if (f in s)]
        if len(matching) != 1:
            print(f'missing file {f}')
            print(f'file list = {list2check}')
            return False
    return True

#image load method
def loadImg(image: Path):
    img = Image.open(image)
    return img

# ---
# backtest

from copy import deepcopy
from finrl.plot import backtest_stats, get_daily_return, get_baseline # backtest_plot
from pyfolio import plotting, utils
import empyrical as ep
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

@plotting.customize
def create_returns_tear_sheet(returns, positions=None,
                              transactions=None,
                              live_start_date=None,
                              cone_std=(1.0, 1.5, 2.0),
                              benchmark_rets=None,
                              bootstrap=False,
                              turnover_denom='AGB',
                              header_rows=None,
                              return_fig=False):
    if benchmark_rets is not None:
        returns = utils.clip_returns_to_benchmark(returns, benchmark_rets)

    plotting.show_perf_stats(returns, benchmark_rets,
                             positions=positions,
                             transactions=transactions,
                             turnover_denom=turnover_denom,
                             bootstrap=bootstrap,
                             live_start_date=live_start_date,
                             header_rows=header_rows)

    plotting.show_worst_drawdown_periods(returns)

    vertical_sections = 11

    if live_start_date is not None:
        vertical_sections += 1
        live_start_date = ep.utils.get_utc_timestamp(live_start_date)

    if benchmark_rets is not None:
        vertical_sections += 1

    if bootstrap:
        vertical_sections += 1

    fig = plt.figure(figsize=(14, vertical_sections * 6))
    gs = gridspec.GridSpec(vertical_sections, 3, wspace=0.5, hspace=0.5)
    ax_rolling_returns = plt.subplot(gs[:2, :])

    i = 2
    ax_rolling_returns_vol_match = plt.subplot(gs[i, :], )

    i += 1
    ax_rolling_returns_log = plt.subplot(gs[i, :], )

    i += 1
    ax_returns = plt.subplot(gs[i, :], )

    i += 1
    if benchmark_rets is not None:
        ax_rolling_beta = plt.subplot(gs[i, :], )
        i += 1

    ax_rolling_volatility = plt.subplot(gs[i, :], )

    i += 1
    ax_rolling_sharpe = plt.subplot(gs[i, :], )

    i += 1
    ax_drawdown = plt.subplot(gs[i, :], )

    i += 1
    ax_underwater = plt.subplot(gs[i, :], )

    i += 1
    ax_monthly_heatmap = plt.subplot(gs[i, 0])
    ax_annual_returns = plt.subplot(gs[i, 1])
    ax_monthly_dist = plt.subplot(gs[i, 2])
    i += 1
    ax_return_quantiles = plt.subplot(gs[i, :])
    i += 1

    plotting.plot_rolling_returns(
        returns,
        factor_returns=benchmark_rets,
        live_start_date=live_start_date,
        cone_std=cone_std,
        ax=ax_rolling_returns)
    ax_rolling_returns.set_title(
        'Cumulative returns')

    plotting.plot_rolling_returns(
        returns,
        factor_returns=benchmark_rets,
        live_start_date=live_start_date,
        cone_std=None,
        volatility_match=(benchmark_rets is not None),
        legend_loc=None,
        ax=ax_rolling_returns_vol_match)
    ax_rolling_returns_vol_match.set_title(
        'Cumulative returns volatility matched to benchmark')

    plotting.plot_rolling_returns(
        returns,
        factor_returns=benchmark_rets,
        logy=True,
        live_start_date=live_start_date,
        cone_std=cone_std,
        ax=ax_rolling_returns_log)
    ax_rolling_returns_log.set_title(
        'Cumulative returns on logarithmic scale')

    plotting.plot_returns(
        returns,
        live_start_date=live_start_date,
        ax=ax_returns,
    )
    ax_returns.set_title(
        'Returns')

    if benchmark_rets is not None:
        plotting.plot_rolling_beta(
            returns, benchmark_rets, ax=ax_rolling_beta)

    plotting.plot_rolling_volatility(
        returns, factor_returns=benchmark_rets, ax=ax_rolling_volatility)

    plotting.plot_rolling_sharpe(
        returns, ax=ax_rolling_sharpe)

    # Drawdowns
    plotting.plot_drawdown_periods(
        returns, top=5, ax=ax_drawdown)

    plotting.plot_drawdown_underwater(
        returns=returns, ax=ax_underwater)

    plotting.plot_monthly_returns_heatmap(returns, ax=ax_monthly_heatmap)
    plotting.plot_annual_returns(returns, ax=ax_annual_returns)
    plotting.plot_monthly_returns_dist(returns, ax=ax_monthly_dist)

    plotting.plot_return_quantiles(
        returns,
        live_start_date=live_start_date,
        ax=ax_return_quantiles)

    if bootstrap and (benchmark_rets is not None):
        ax_bootstrap = plt.subplot(gs[i, :])
        plotting.plot_perf_stats(returns, benchmark_rets,
                                 ax=ax_bootstrap)
    elif bootstrap:
        raise ValueError('bootstrap requires passing of benchmark_rets.')

    for ax in fig.axes:
        plt.setp(ax.get_xticklabels(), visible=True)

    if return_fig:
        return fig

def backtest_plot(
        account_value,
        baseline_df,
        value_col_name="account_value",
):
    df = deepcopy(account_value)
    # print('date', len(df))
    # print(type(df["date"][0]), df["date"][0])
    df["date"] = pd.to_datetime(df["date"])
    # df["date"] = pd.Timestamp(df["date"]).tz_localize("America/New_York")
    # df["date"] = df["date"].tz_localize("America/New_York")
    test_returns = get_daily_return(df, value_col_name=value_col_name)
    test_returns.fillna(0, inplace=True)  # the first day is nan

    baseline_df["date"] = pd.to_datetime(baseline_df["date"], format="%Y-%m-%d")
    baseline_df = pd.merge(df[["date"]], baseline_df, how="left", on="date")
    # import  pdb; pdb.set_trace()
    # baseline_df = baseline_df.fillna(method="ffill").fillna(method="bfill")
    baseline_returns = get_daily_return(baseline_df, value_col_name="close")
    baseline_returns.fillna(0, inplace=True) # the first day is nan

    with pyfolio.plotting.plotting_context(font_scale=1.1):
        # this will return figs: https://github.com/quantopian/pyfolio/blob/master/pyfolio/tears.py ; create_full_tear_sheet will not
        figs = create_returns_tear_sheet(
            returns=test_returns, benchmark_rets=baseline_returns, set_context=False, return_fig=True
        )

    return figs
