"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks (Part 2)

Description
==============================================================
This module contains the code to process, clean and merge the
necessary data from the Yahoo Finance and Macrotrends website.

Copyright and Usage Information
==============================================================

This file is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""
from urllib.error import HTTPError  # Same case
import csv
import math
import pandas as pd
import requests
from lxml import etree  # This is only used for except statement. This is auto imported by pandas.
from yahoofinancials import YahooFinancials
# from python_ta.contracts import check_contracts


# @check_contracts
def read_csv() -> list[str]:
    """Load data from csv file (filled with names of stocks) and return it in a list
    """
    csv_file = 'good&bad_stocks.csv'
    stocks_list = []
    with open(csv_file) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skips first line
        for row in reader:
            stocks_list.extend(row)
    return stocks_list


# @check_contracts
def filter_stocks(stock_list: list[str], end_date: str) -> list[str]:
    """
    This function filter out stocks that data cannot be retrieved from and only
    return stocks that the Yahoo Finance API has data on.

    Preconditions:
        - end_date must be in the format of "YYYY-MM-DD"
        - stock_list != ""

    >>> filter_stocks(['AAPL', 'MSFT'], '2010-01-01')
    ['AAPL', 'MSFT']
    """
    list_so_far = []
    for stock in stock_list:
        try:
            filter_stock = get_percentage_growth(stock, end_date)
            if isinstance(filter_stock, float):
                list_so_far.append(stock)
        # Do not add stock if they cause one of these errors
        except (KeyError, IndexError, ValueError, TypeError, ImportError, AssertionError, ConnectionResetError, OSError
                ):
            continue
    return list_so_far


# @check_contracts
def get_percentage_growth(stock: str, end_date: str) -> float:
    """
    Returns the percentage growth of the stock from start date (the year 2009) to <end_date> (the user inputs end_date)

    To calculate the percentage gain/loss in a stock, the end date price is subtracted from start date price.
    Then it is divided by the start date price. Lastly, multiply the result by 100 to get the percentage change.
    As a formula -> ((end price - start price) / start price) * 100

    Preconditions:
        - end_date must be in the format of "YYYY-MM-DD"
        - stock != ""
    """
    yahoo_financials = YahooFinancials(stock)
    data = yahoo_financials.get_historical_price_data("2009-01-01", end_date, "daily")  # Extract data
    prices = data[stock]['prices']
    initial_price = prices[0]['adjclose']
    recent_price = prices[len(prices) - 1]['adjclose']
    calc_percentage = ((recent_price - initial_price) / initial_price) * 100    # Formula for growth percentage
    return calc_percentage


# @check_contracts
def get_percentage_growth_of_stocks(stock_list: list[str], end_date: str) -> list[tuple[str, float]]:
    """
    Returns a sorted list of tuples based on the percentage growth of each stock (biggest to smallest).
    Each tuple is of the form (stock, percentage growth). Each stock corresponds to their <get_percentage_growth> value.

    Preconditions:
        - end_date must be in the format of "YYYY-MM-DD"
        - stock_list != []
    """
    list_so_far = []
    for stock in stock_list:
        try:
            list_so_far.append((stock, get_percentage_growth(stock, end_date)))
        # Do not add stock if they cause one of these errors
        except (KeyError, IndexError, ValueError, TypeError, ImportError, AssertionError, ConnectionResetError, OSError
                ):
            continue
    sorted_list = sorted(list_so_far, key=lambda x: x[1], reverse=True)
    return sorted_list


# @check_contracts
def top_half(sorted_list: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """
    Returns good stocks (top half) list from get_percentage_growth_of_stocks output.
    Since <get_percentage_growth_of_stocks> returns a sorted list based on biggest to the smallest percentage growth,
    top_half returns a list with stocks that have good percentage growths

    Preconditions:
        - sorted_list != [] and len(sorted_list) >= 2

    >>> top_half([('AAPL', 132.20943095468306), ('MSFT', 53.44226321349688)])
    [('AAPL', 132.20943095468306)]
    """
    half_list = sorted_list[:len(sorted_list) // 2]  # Takes top half
    return half_list


# @check_contracts
def obtain_factor_data(link: str, get_price: bool) -> pd.DataFrame | pd.Series:
    """
    Return DataFrame historical data of stock. The DataFrame is in the form of two columns.
    The left column consists of years and the right column consists of the corresponding data from each year based
    on the factor (input of <link>).

    Preconditions:
        - link in ['pe-ratio', 'price-sales', 'price-book', 'roe', 'roa', 'return-on-tangible-equity',
             'number-of-employees', 'current-ratio', 'quick-ratio', 'total-liabilities',
             'debt-equity-ratio', 'roi', 'cash-on-hand', 'total-share-holder-equity', 'revenue', 'gross-profit',
             'net-income', 'shares-outstanding', 'stock-price-history']
    """
    # IMPORTANT:
    # This code was actually very simple. I was using pandas' iloc method.
    # However, python-ta causes error saying contact instructor with error message.
    # But since Professor and TA is not replying to our question, I changed iloc to filter method.
    # Thus, code got a bit complicated.
    data = pd.read_html(link, skiprows=1)
    df = pd.DataFrame(data[0])  # Skip header
    df = pd.concat([df.columns.to_frame().T, df], ignore_index=True)  # Make it to frame
    df.columns = range(len(df.columns))
    df = df[1:]
    # Average price and stock price is on the same page, thus, function needs to split the cases.
    if get_price is False:
        if 'stock-price-history' in link:
            df = df.filter(items=[df.columns[0], df.columns[1]])  # Get average price
        else:
            df = df.filter(items=[df.columns[0], df.columns[-1]])  # Get other factors data
    else:
        df = df.filter(items=[df.columns[0], df.columns[-2]])  # Get stock price
    return df


# @check_contracts
def get_factors_data(stock: str, factors: list[str]) -> dict[str, pd.DataFrame | pd.Series]:
    """
    Return DataFrame of historical factor of stock. The DataFrame has the same function as obtain_factor_data but
    instead of only showing data for one factor, it will show data from all factors in the factor list <links>.

    Preconditions:
        - stock != ''
        - factors != []
    """
    url = f'https://www.macrotrends.net/stocks/charts/{stock}/'
    response = requests.get(url)
    new_url = str(response.url)

    links = factors + ['stock-price-history']
    # 'stock-price-history' here gets average price as well as stock price

    dict_df = {}
    for link in links:
        combined_link = str(new_url + link)
        if link == 'stock-price-history':
            # Rename to average_price
            dict_df['average-price'] = obtain_factor_data(combined_link, get_price=False)
        else:
            dict_df[link] = obtain_factor_data(combined_link, get_price=False)
    # Get price of stock
    dict_df['price'] = obtain_factor_data(str(new_url + 'stock-price-history'), get_price=True)
    return dict_df


# @check_contracts
def clean_and_merge_data(factor: str, dict_df: dict[str, pd.DataFrame | pd.Series],
                         end_date: str) -> pd.DataFrame | pd.Series:
    """
    Function cleans the data, then merges price data and factor data into one DataFrame.

    First, this function gets the data of the stock price and the factor values.
    It cleans up missing and incorrect values in the year column and converts each year into integer.
    Then the data that is before and including the end date is chosen.
    The year column is then removed and the remaining data is turned into float.
    Lastly, function merges price and factor data into one DataFrame.

    Preconditions:
        - factor != ""
        - end_date must be in the format of "YYYY-MM-DD"
        - dict_df != {}
    """
    # IMPORTANT:
    # This code was actually very simple. I was using pandas' iloc method.
    # However, python-ta causes error saying contact instructor with error message.
    # But since Professor and TA is not replying to our question, I changed iloc to filter method.
    # Thus, code got a bit complicated.
    end_year = int(end_date.split('-')[0])  # Take year only and change to integer.

    df1 = dict_df['price']
    df2 = dict_df[factor]
    min_rows = min(df1.shape[0], df2.shape[0])  # Take minimum rows.
    df1 = df1.head(min_rows)  # Using ^ above variable, cut out the rows and merge them together as same length of rows.
    df2 = df2.head(min_rows)
    # Used to be iloc, but changed to using filter. This merges two DataFrames into one.
    merged_df = pd.concat([df1, df2.filter(items=[df2.columns[-1]])], axis=1)
    # Originally there was an error where it would return an empty dataframe. So dropping NaN is important.
    merged_df.dropna(inplace=True)  # Drop NaN.

    # Change the date column into integers
    try:
        merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].astype(int)
        # If this doesn't work, first need to remove '-' dash and then convert to integer.
    except ValueError:
        merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].str.replace('-', '', regex=True).astype(int)

    # Select dates up to end date.
    # '<=' inequality is needed to select one with correct end year.
    merged_df = merged_df.loc[merged_df[0] <= end_year].reset_index(drop=True)

    merged_df = merged_df.filter(items=[merged_df.columns[-2], merged_df.columns[-1]])  # Deletes dates
    merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].astype(float)  # Convert to float type.
    try:
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].astype(float)  # If not work, then use except.
    except ValueError:  # Remove unnecessary symbols and then convert to float.
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace('$', '', regex=True)
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace('%', '', regex=True)
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace(',', '', regex=True).astype(float)

    return merged_df


# @check_contracts
def correlation(merged_df: pd.DataFrame | pd.Series) -> float:
    """
    Returns the correlation of a single factor to  the stock price.
    """
    price_vs_factor_correlation = merged_df.corr(numeric_only=True)  # By default, pearson method.
    # Takes the correlation of merged DataFrame
    return price_vs_factor_correlation[price_vs_factor_correlation.columns[1]][price_vs_factor_correlation.columns[0]]


# @check_contracts
def all_factors_correlation(stock: str, end_date: str, factors: list[str]) -> dict[str, float]:
    """
    Returns a dictionary of correlations in which the key is the factor in <factors> and the value is the
    correlation value based on the factor. Factor 'average-price' will be included as minimum requirement.

    Preconditions:
        - stock != ''
        - end_date must be in the format of "YYYY-MM-DD"
        - factors != []

    >>> all_factors_correlation('AAPL', '2010-01-01', ['pe-ratio'])
    {'pe-ratio': 0.7035086230529171, 'average-price': 0.9644461603074899}
    """
    dict_df = get_factors_data(stock, factors)
    copy_factors = factors + ['average-price']  # We don't want to mutate, thus make copy
    dict_of_correlations = {}
    for factor in copy_factors:
        cleaned_data = clean_and_merge_data(factor, dict_df, end_date)  # Clean and merge to DataFrame
        dict_of_correlations[factor] = correlation(cleaned_data)  # Get correlation and save to dict
    return dict_of_correlations


# @check_contracts
def filter_nan(factors_correlation: dict[str, float]) -> bool:
    """
    Return False if one of values in <factors_correlation> is NaN

    Preconditions:
        - factors_correlation != {}
    """
    for value in factors_correlation.values():
        if math.isnan(value):  # Check if one of value is NaN
            return False
    return True


# @check_contracts
def determining_best_factor(top_ranked_stocks: list[tuple[str, float]], end_date: str, factors: list[str]) \
        -> list[tuple[str, float]]:
    """
    Returns a sorted list of tuples based on the order which starts from worst factor to best factor.

    Preconditions:
        - top_ranked_stocks != []
        - end_date must be in the format of "YYYY-MM-DD"
        - factors != []
    """
    lst_of_dict = []
    for top_stock in top_ranked_stocks:  # Collects all correlation values
        try:
            factors_correlation = all_factors_correlation(top_stock[0], end_date, factors)
            if not filter_nan(factors_correlation):  # Filter out the NaN
                continue
            lst_of_dict.append(all_factors_correlation(top_stock[0], end_date, factors))
        except (etree.XMLSyntaxError, HTTPError):
            continue

    average_factor_correlation = {}
    for factor in lst_of_dict[0].keys():  # Take the average of all correlation values of each factor
        combined_tuple = tuple(each_top_stock[factor] for each_top_stock in lst_of_dict)
        average_factor_correlation[factor] = sum(combined_tuple) / len(combined_tuple)

    convert_to_tuple = list((factor_name, correlation_value) for factor_name, correlation_value in
                            average_factor_correlation.items())
    sorted_tuple = sorted(convert_to_tuple, key=lambda x: x[1])  # Sort factors based on their average correlation value
    return sorted_tuple


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['yahoofinancials', 'pandas', 'requests', 'csv', 'lxml', 'urllib.error', 'math'],
        'max-line-length': 120,
        'allowed-io': ['read_csv']  # the names (strs) of functions that call print/open/input
    })
