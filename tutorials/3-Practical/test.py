from finrl.meta.preprocessor.yahoodownloader import YahooDownloader



def get_baseline(ticker, start, end):
    return YahooDownloader(
        start_date=start, end_date=end, ticker_list=[ticker]
    ).fetch_data()


test_start_date = '2022-6-11'
test_end_date = '2023-1-2'
baseline_ticker = 'AXP'

baseline_df = get_baseline(            
                ticker = baseline_ticker, 
                start = test_start_date,
                end = test_end_date)
