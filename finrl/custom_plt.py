from pyfolio import plotting, utils
import empyrical as ep
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyfolio import timeseries


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
    APPROX_BDAYS_PER_MONTH = 21

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
        returns, factor_returns=benchmark_rets, ax=ax_rolling_volatility, 
        rolling_window=APPROX_BDAYS_PER_MONTH * 1)  # make shorter

    plotting.plot_rolling_sharpe(
        returns, ax=ax_rolling_sharpe,
        rolling_window=APPROX_BDAYS_PER_MONTH * 1)  # make shorter

    # Drawdowns  error: matplotlib.units.ConversionError: Failed to convert value(s) to axis units: (NaT, Timestamp('2022-12-30 00:00:00+0000', tz='UTC'))
    # plotting.plot_drawdown_periods(
    #     returns, top=5, ax=ax_drawdown)

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


def cal_returns_tear_sheet(returns):
    result = dict()
    # Cumulative returns
    cumulative_returns = ep.cum_returns(returns, 1.0)
    result['returns'] = returns
    result['cumulative_returns'] = cumulative_returns

    # rolling_volatility
    APPROX_BDAYS_PER_MONTH = 21
    rolling_window = APPROX_BDAYS_PER_MONTH * 1  # minimum time
    rolling_vol_ts = timeseries.rolling_volatility(
        returns, rolling_window)
    result['rolling_volatility'] = rolling_vol_ts

    # rolling_sharpe
    rolling_sharpe_ts = timeseries.rolling_sharpe(
        returns, rolling_window)
    result['rolling_sharpe'] = rolling_sharpe_ts

    # drawdown
    top = 10
    df_drawdowns = timeseries.gen_drawdown_table(returns, top=top)
    result['drawdowns'] = df_drawdowns

    # drawdown underwater
    df_cum_rets = ep.cum_returns(returns, starting_value=1.0)
    running_max = np.maximum.accumulate(df_cum_rets)
    underwater = -100 * ((running_max - df_cum_rets) / running_max)
    result['drawdown_underwater'] = underwater

    # monthly_returns
    monthly_ret_table = ep.aggregate_returns(returns, 'monthly')
    result['monthly_returns'] = monthly_ret_table

    # annual_returns
    ann_ret_df = ep.aggregate_returns(returns, 'yearly')
    result['yearly_returns'] = ann_ret_df

    # TODO rolling_beta: requires baseline
    return result



if __name__ == "__main__":
    test_returns = pd.read_csv('test_returns.csv')
    test_returns['date'] = pd.to_datetime(test_returns['date'])
    test_returns = test_returns.set_index('date')['daily_return']
    result = cal_returns_tear_sheet(test_returns)
    print(result)