from yahoofinancials import YahooFinancials
import pandas as pd
import requests
import csv

# 1. data
# stocks = input("Type list of stocks to possibibly invest, e.g. ['AAPL', 'META', 'MSFT']: ")
# train_end_date = str(input(
#     "Initial training date is 2009. Type end date you want to train the model. e.g. 2015-03-25: "))


def read_csv() -> list[str]:
    """Load data from csv file and return it to list
    """
    csv_file = 's&p500.csv'
    stocks_list = []
    with open(csv_file) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skips first line
        for row in reader:
            stocks_list.extend(row)
    return stocks_list


def get_percentage_growth(stock: str, end_date: str) -> float:
    """
    Returns the percentage growth of the stock from start date (the year 2009) to end_date (the user inputs end_date)

    To calculate the percentage gain/loss in a stock, the end date price is subtracted from start date price.
    Then it is divided by the start date price. Lastly, multiply the result by 100 to get the percentage change.
    As a formula -> ((end price - start price) / start price) * 100

    Preconditions:
        - end_date must be in the format of "YYYY-MM-DD"
        - isinstance(user_input, str)
        - user_input != ""
    """
    yahoo_financials = YahooFinancials(stock)
    data = yahoo_financials.get_historical_price_data("2009-01-28", end_date, "daily")
    prices = data[stock]['prices']
    initial_price = prices[0]['adjclose']
    recent_price = prices[len(prices) - 1]['adjclose']
    calc_percentage = ((recent_price - initial_price) / initial_price) * 100
    return calc_percentage

    # from datetime import datetime, timedelta
    # yahoo_financials = YahooFinancials(stock)
    # stats = (yahoo_financials.get_historical_price_data("2009-01-27", "2009-01-28", 'daily'))
    # initial_price = float(stats[stock]['prices'][0]['adjclose'])
    # end_date_minus_one = datetime.strptime(end_date, '%Y-%m-%d')
    # end_date_minus_one = end_date_minus_one.date() + timedelta(days=1)
    # stats = (yahoo_financials.get_historical_price_data(end_date, end_date_minus_one.strftime('%Y-%m-%d'), 'daily'))
    # recent_price = float(stats[stock]['prices'][0]['adjclose'])
    # calc_percentage = ((recent_price - initial_price) / initial_price) * 100
    # return calc_percentage


def get_percentage_growth_of_stocks(stock_list: list[str], end_date: str) -> list[tuple[str, float]]:
    """
    Returns a sorted list of tuples based on the percentage growth of each stock (biggest to smallest).
    Each tuple is of the form (stock, growth percentage).

    Preconditions:
        - end_date must be in the format of "YYYY-MM-DD"
        - isinstance(user_input, list)
        - user_input != []
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
    Returns good stocks (top half) list from retrieve_percentage_growth_of_stocks output
    """
    half_list = sorted_list[:len(sorted_list)//2]
    return half_list


def obtain_factor_data(link: str, get_price: bool) -> pd.DataFrame | pd.Series:
    """Get historical data of stock.

    Preconditions:
        - stock != ''
        - isinstance(stock, str)
    """
    data = pd.read_html(link, skiprows=1)
    df = pd.DataFrame(data[0])
    df = pd.concat([df.columns.to_frame().T, df], ignore_index=True)
    df.columns = range(len(df.columns))
    df = df[1:]
    # Average price and stock price is on the same page, thus, I need to split the cases.
    if get_price is False:
        if 'stock-price-history' in link:
            df = df.iloc[:, [0, 1]]  # Get average price
        else:
            df = df.iloc[:, [0, -1]]  # Get other factors data
    else:
        df = df.iloc[:, [0, -2]]  # Get stock price
    return df


def get_factors_data(stock: str) -> dict[str, pd.DataFrame | pd.Series]:
    """
    Return DataFrame of historical factor of stock.

    Preconditions:
        - stock != ''
        - isinstance(stock, str)
    """
    url = f'https://www.macrotrends.net/stocks/charts/{stock}/'
    response = requests.get(url)
    new_url = str(response.url)

    links = ['pe-ratio', 'price-sales', 'price-book', 'roe', 'roa', 'return-on-tangible-equity',
             'number-of-employees', 'current-ratio', 'quick-ratio', 'total-liabilities',
             'debt-equity-ratio', 'roi', 'cash-on-hand', 'total-share-holder-equity', 'revenue', 'gross-profit',
             'net-income', 'shares-outstanding', 'stock-price-history']
    # stock-price-history here gets average price as well as stock price

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


def correlation(factor: str, dict_df: dict[str, pd.DataFrame | pd.Series]) -> float:
    df1 = dict_df['price']
    df2 = dict_df[factor]
    min_rows = min(df1.shape[0], df2.shape[0])
    df1 = df1.iloc[:min_rows]
    df2 = df2.iloc[:min_rows]
    merged_df = pd.concat([df1, df2.iloc[:, -1]], axis=1)
    merged_df.dropna(inplace=True)

    merged_df = merged_df.iloc[:, -2:]
    merged_df[merged_df.columns[0]] = merged_df[merged_df.columns[0]].astype(float)
    try:
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].astype(float)
    except ValueError:
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace('$', '', regex=True)
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace('%', '', regex=True)
        merged_df[merged_df.columns[1]] = merged_df[merged_df.columns[1]].str.replace(',', '', regex=True).astype(float)

    price_vs_factor_correlation = merged_df.corr(numeric_only=True)  # By default, pearson method.
    # method = 'pearson', 'spearman'

    return price_vs_factor_correlation[price_vs_factor_correlation.columns[1]][price_vs_factor_correlation.columns[0]]


def all_factors_correlation(stock: str) -> dict[str, float]:
    dict_df = get_factors_data(stock)
    factors = ['pe-ratio', 'price-sales', 'price-book', 'roe', 'roa', 'return-on-tangible-equity',
               'number-of-employees', 'current-ratio', 'quick-ratio', 'total-liabilities',
               'debt-equity-ratio', 'roi', 'cash-on-hand', 'total-share-holder-equity', 'revenue', 'gross-profit',
               'net-income', 'shares-outstanding', 'average-price']
    dict_of_correlations = {}
    for factor in factors:
        dict_of_correlations[factor] = correlation(factor, dict_df)
    return dict_of_correlations
# sort lambda


# standard deviation -> dataframe.std()
# df['Col'].std()
