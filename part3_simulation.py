from datetime import datetime
from yahoofinancials import YahooFinancials
from part2_recommendation_tree import RecommendationTree
import part1_factor_data_processing

stocks = ['MSFT', 'META']
initial_investment = 10000


def get_price(stock: str, year: int) -> float:
    yahoo_financials = YahooFinancials(stock)
    data = yahoo_financials.get_historical_price_data(str(year) + '-01-01', str(year) + '-01-05', "daily")
    prices = data[stock]['prices']
    recent_price = prices[len(prices) - 1]['adjclose']
    return recent_price


def benchmark_simulation(benchmark: str, start_date: str) -> dict[int, float]:
    """
    Function is using either NASDAQ or S&P500 as a benchmark.
    Creates a simulation starting from start date (which is the year after the data ends) to the
    end date (which is today's year).
    This benchmark simulates how much the user will earn if the capital was invested into S&P500
    or NASDAQ from start_date till most recent year
    - '^GSPC' stands for S&P500
    - '^IXIC' stands for NASDAQ
    Function outputs the date of year and the percentage profit made each year.
    E.g. {2016: 0.0, 2017: 12.823326415655877, 2018: 35.34277741767793, ... 2023: 91.43670094654134}
    """
    record_percenage_for_each_year = {}
    start_year = int(start_date.split('-')[0]) + 1
    end_year = int(datetime.today().strftime('%Y'))  # Convert string end_date to int
    initial_price = get_price(benchmark, start_year)
    for each_year in range(start_year, end_year + 1):
        recent_price = get_price(benchmark, each_year)
        calc_percentage = ((recent_price - initial_price) / initial_price) * 100
        record_percenage_for_each_year[each_year] = calc_percentage
    return record_percenage_for_each_year


def recommendation_tree_simulation(stocks: list[str], initial_investment: float, start_date: str,
                                   risk_percentage: int, recommendation_tree: RecommendationTree) -> dict[int, float]:
    """
    Preconditions:
        - 1 <= risk_percentage <= 100

    Creates a simulation starting from start date (which is the year after the data ends) to the
    end date (which is today's year).
    Here's what function does:
    1. User input want to invest stocks and risk percentage, i.e., risk percentage 50% is input as 50
    2. Function generates a complete recommendation tree
    3. Function invests in most prominent stocks in the list of stocks by using then recommendation
    tree and risk factor
    4. Each year, function will decide whether to buy, hold or sell the stocks as per recommendation tree
    5. Function outputs the date of year and the percentage profit made each year.
    E.g. {2016: 0.0, 2017: 12.823326415655877, 2018: 35.34277741767793, ... 2023: 91.43670094654134}
    """
    start_year = int(start_date.split('-')[0]) + 1
    end_year = int(datetime.today().strftime('%Y'))  # Convert string end_date to int

    record_percenage_for_each_year = {}

    stocks_in_position = {}
    total_profits = 0
    profits = 0

    total_capitial = initial_investment

    for each_year in range(start_year, end_year + 1):
        recommendation_tree.remove_list_of_stocks()
        for stock in stocks:  #Classify each stock into game_tree
            recommendation_tree.move_stock_to_subtree(
                (stock, part1_factor_data_processing.all_factors_correlation(stock, end_date=str(each_year) + '-01-01'))
            )
        ranked_choices = recommendation_tree.ranked_choices_of_stocks()
        range_of_buy_leafs = len(ranked_choices) - ((len(ranked_choices) * risk_percentage) // 100)
        nested_buy_stocks = [ranked_choices[choices] for choices in ranked_choices if
                             choices > range_of_buy_leafs and ranked_choices[choices] != []]  # Drop empty list and
        # pick ranked list of stocks based on percentage risk
        buy_stocks = [item for sublist in nested_buy_stocks for item in sublist]  # Converts nested list to flat list
        # part3_simulation.recommendation_tree_simulation(['MSFT', 'META'], 355, '2015-4', 50, recommendation_tree)
        ############################################################################################
        profit_percentage = 0
        max_capitial_to_use_for_each_stock = total_capitial // len(stocks)
        for each_stock in stocks:
            if each_stock in buy_stocks and each_stock not in stocks_in_position:
                # buy
                # price_of_stock = get_price(each_stock, end_year)
                # num_of_shares = max_capitial_to_use_for_each_stock // price_of_stock
                # total_price_of_shares = price_of_stock * num_of_shares
                # bought_list_of_stocks[each_stock] =
                # total_capitial -= total_price_of_shares
            elif each_stock in buy_stocks and each_stock in stocks_in_position:
                # hold
            else:
                if each_stock in stocks_in_position:
                    # sell
                pass



        #
        #     holding_price = number_of_shares_to_hold * price_of_stock
        #     total_holding_capitial += holding_price
        #
        # record_investment_for_each_year[each_year] = total_holding_capitial
