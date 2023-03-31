"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks (Part 3)

Instructions (READ THIS FIRST!)
===============================

...

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""

from datetime import datetime
from yahoofinancials import YahooFinancials


def get_price(stock: str, year: int) -> float:
    """
    Function gets the stock price at the current year
    Preconditions:
    - stock! = ''
    - Must be an existing year
    """
    yahoo_financials = YahooFinancials(stock)
    data = yahoo_financials.get_historical_price_data(str(year) + '-01-01', str(year) + '-01-05', "daily")
    prices = data[stock]['prices']
    recent_price = prices[len(prices) - 1]['adjclose']
    return recent_price


def benchmark_simulation(benchmark: str | list[str], start_date: str) -> dict[int, float]:
    """
    Function is using either NASDAQ or S&P500 as a benchmark.
    Creates a simulation starting from start date (which is the year after the data ends) to the
    end date (which is today's year).
    This benchmark simulates how much the user will earn if the capital was invested into S&P500
    or NASDAQ from start_date till most recent year
    - '^IXIC' stands for NASDAQ
    - '^GSPC' stands for S&P500
    Function outputs the date of year and the percentage profit made each year.
    E.g. {2016: 0.0, 2017: 12.823326415655877, 2018: 35.34277741767793, ... 2023: 91.43670094654134}

    Preconditions:
        - benchmark in {'^IXIC', '^GSPC'} or benchmark != []
        - len(start_date) == 10
        - start_date[4] == start_date[7] == '-'
        - int(start_date[:4]) >= 2009
    """
    record_percenage_for_each_year = {}
    start_year = int(start_date.split('-')[0]) + 1
    end_year = int(datetime.today().strftime('%Y'))  # Convert string end_date to int

    if isinstance(benchmark, str):
        initial_price = get_price(benchmark, start_year)
        for each_year in range(start_year, end_year + 1):
            recent_price = get_price(benchmark, each_year)
            calc_percentage = ((recent_price - initial_price) / initial_price) * 100
            record_percenage_for_each_year[each_year] = calc_percentage
    else:
        initial_price = 0
        for each_stock in benchmark:
            initial_price += get_price(each_stock, start_year)
        for each_year in range(start_year, end_year + 1):
            recent_price = 0
            for each_stock in benchmark:
                recent_price += get_price(each_stock, each_year)
            calc_percentage = ((recent_price - initial_price) / initial_price) * 100
            record_percenage_for_each_year[each_year] = calc_percentage

    return record_percenage_for_each_year


def recommendation_tree_simulation(buy_stocks: list[str], start_date: str) -> dict[int, float]:
    """
    Creates a simulation starting from start date (which is the year after the data ends) to the
    end date (which is today's year).
    Here's what function does:
    1. User gives list of stocks and start date
    2. Function creates a recommendation tree and decides which stocks to buy
    3. Calls the determining buy stocks option and buys according to risk factor
    4. Holds the stocks from start_date till present year and sells them
    5. Retuns profit for ach year
    """
    start_year = int(start_date.split('-')[0]) + 1
    end_year = int(datetime.today().strftime('%Y'))  # Convert string end_date to int
    record_percenage_for_each_year = {}

    initial_price = 0
    if not buy_stocks == []:
        for each_stock in buy_stocks:
            initial_price += get_price(each_stock, start_year)
    for each_year in range(start_year, end_year + 1):
        recent_price = 0
        if not buy_stocks == []:
            for each_stock in buy_stocks:
                recent_price += get_price(each_stock, each_year)
        calc_percentage = 0  # This ensures that function do not divide by 0
        if not buy_stocks == []:
            calc_percentage = ((recent_price - initial_price) / initial_price) * 100
        record_percenage_for_each_year[each_year] = calc_percentage
    return record_percenage_for_each_year
