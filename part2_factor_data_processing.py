"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks (Part 1)

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
from yahoofinancials import YahooFinancials
import pandas as pd
import requests
import csv
from lxml import etree  # This is only used for except statement. This is auto imported by pandas.
from urllib.error import HTTPError  # Same case
import math


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

def filter_stocks(stock_list: list[str], end_date: str) -> list[str]:
    """
    This function filter out stocks that data cannot be retrieved from and only
    return stocks that the Yahoo Finance API has data on.

    Preconditions:
        - end_date must be in the format of "YYYY-MM-DD"
        - stock_list != ""
    """
    list_so_far = []
    for stock in stock_list:
        try:
            filter_stock = get_percentage_growth(stock, end_date)
            if isinstance(filter_stock, float):
                list_so_far.append(stock)
        except(KeyError, IndexError, ValueError, TypeError, ImportError, AssertionError, ConnectionResetError, OSError):
            continue
    return list_so_far


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
    calc_percentage = ((recent_price - initial_price) / initial_price) * 100
    return calc_percentage


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
        except(KeyError, IndexError, ValueError, TypeError, ImportError, AssertionError, ConnectionResetError, OSError):
            continue
    sorted_list = sorted(list_so_far, key=lambda x: x[1], reverse=True)
    return sorted_list


def top_half(sorted_list: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """
    Returns good stocks (top half) list from get_percentage_growth_of_stocks output.
    Since <get_percentage_growth_of_stocks> returns a sorted list based on biggest to the smallest percentage growth,
    top_half returns a list with stocks that have good percentage growths

    Preconditions:
        - sorted_list != []
    """
    half_list = sorted_list[:len(sorted_list)//2]
    return half_list


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
    data = pd.read_html(link, skiprows=1)
    df = pd.DataFrame(data[0])  # Skip header
    df = pd.concat([df.columns.to_frame().T, df], ignore_index=True)  # Make it to frame
    df.columns = range(len(df.columns))
    df = df[1:]
    # Average price and stock price is on the same page, thus, function needs to split the cases.
    if get_price is False:
        if 'stock-price-history' in link:
            df = df.iloc[:, [0, 1]]  # Get average price
        else:
            df = df.iloc[:, [0, -1]]  # Get other factors data
    else:
        df = df.iloc[:, [0, -2]]  # Get stock price
    return df

def get_factors_data(stock: str, factors: list[str]) -> dict[str, pd.DataFrame | pd.Series]:
    """
    Return DataFrame of historical factor of stock. The DataFrame has the same function as obtain_factor_data but
    instead of only showing data for one factor, it will show data from all factors in the factor list <links>.

    Preconditions:
        - stock != ''
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
    end_year = int(end_date.split('-')[0])

    df1 = dict_df['price']
    df2 = dict_df[factor]
    min_rows = min(df1.shape[0], df2.shape[0])
    df1 = df1.iloc[:min_rows]
    df2 = df2.iloc[:min_rows]
    merged_df = pd.concat([df1, df2.iloc[:, -1]], axis=1)
    merged_df.dropna(inplace=True)  # Drop NaN

    # Change the date column into integers
    try:
        merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].astype(int)
    except ValueError:
        merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].str.replace('-', '', regex=True).astype(int)

    # Select dates up to end date.
    merged_df = merged_df.loc[merged_df[0] <= end_year].reset_index(drop=True)

    merged_df = merged_df.iloc[:, -2:]  # Deletes dates
    merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].astype(float)
    try:
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].astype(float)
    except ValueError:
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace('$', '', regex=True)
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace('%', '', regex=True)
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace(',', '', regex=True).astype(float)

    return merged_df


def correlation(merged_df: pd.DataFrame | pd.Series) -> float:
    """
    Returns the correlation of a single factor to stock price.

    Preconditions:
        - factor != ''
        - dict_df != {}
    """
    price_vs_factor_correlation = merged_df.corr(numeric_only=True)  # By default, pearson method.
    # method = 'pearson', 'spearman'
    return price_vs_factor_correlation[price_vs_factor_correlation.columns[1]][price_vs_factor_correlation.columns[0]]

def all_factors_correlation(stock: str, end_date: str, factors: list[str]) -> dict[str, float]:
    """
    Returns a dictionary of correlations in which the key is the factor in <factors> and the value is the
    correlation value based on the factor.

    Preconditions:
        - stock != ''
        - end_date must be in the format of "YYYY-MM-DD"
    """
    dict_df = get_factors_data(stock, factors)
    copy_factors = factors + ['average-price']
    # factors = ['pe-ratio', 'price-sales', 'average-price']
    dict_of_correlations = {}
    for factor in copy_factors:
        cleaned_data = clean_and_merge_data(factor, dict_df, end_date)
        dict_of_correlations[factor] = correlation(cleaned_data)
    return dict_of_correlations
# sort lambda

def filter_nan(factors_correlation: dict[str, float]) -> bool:
    """
    Return False if one of values in <factors_correlation> is NaN

    Preconditions:
        - factors_correlation != {}
    """
    for value in factors_correlation.values():
        if math.isnan(value):
            return False
    return True


def determining_best_factor(top_ranked_stocks: list[tuple[str, float]], end_date: str, factors: list[str]) \
        -> list[tuple[str, float]]:
    """
    Returns a sorted list of tuples based on the order which starts from worst factor to best factor.

    Preconditions:
        - top_ranked_stocks != []
        - end_date must be in the format of "YYYY-MM-DD"
    """
    lst_of_dict = []
    for top_stock in top_ranked_stocks:
        try:
            factors_correlation = all_factors_correlation(top_stock[0], end_date, factors)
            if not filter_nan(factors_correlation):
                continue
            lst_of_dict.append(all_factors_correlation(top_stock[0], end_date, factors))
        except (etree.XMLSyntaxError, HTTPError):
            continue
    #   raise XMLSyntaxError("no text parsed from document", 0, 0, 0)
    #   File "<string>", line 0
    # lxml.etree.XMLSyntaxError: no text parsed from document

    average_factor_correlation = {}
    for factor in lst_of_dict[0].keys():
        combined_tuple = tuple(each_top_stock[factor] for each_top_stock in lst_of_dict)
        average_factor_correlation[factor] = sum(combined_tuple) / len(combined_tuple)

    convert_to_tuple = [(factor, correlation_value) for factor, correlation_value in average_factor_correlation.items()]
    sorted_tuple = sorted(convert_to_tuple, key=lambda x: x[1])
    return sorted_tuple
