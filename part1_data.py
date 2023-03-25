from yahoofinancials import YahooFinancials
import pandas as pd
import requests

# 1. data
# stocks = input("Type list of stocks to possibibly invest, e.g. ['AAPL', 'META', 'MSFT']: ")
# train_end_date = str(input(
#     "Initial training date is 2009. Type end date you want to train the model. e.g. 2015-03-25: "))
stocks = ['AAPL', 'MSFT']
train_end_date = '2015-03-25'


def retrieve_percentage_growth(stock: str, end_date: str) -> float:
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


def retrieve_percentage_growth_of_stocks(stock_list: list[str], end_date: str) -> list[tuple[str, float]]:
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
        list_so_far.append((stock, retrieve_percentage_growth(stock, end_date)))
    sorted_list = sorted(list_so_far, key=lambda x: x[1], reverse=True)
    return sorted_list


def get_one_data_from_link(link: str) -> pd.DataFrame | pd.Series:
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
    return df


def historical_factor_datas_for_stock(stock: str) -> pd.DataFrame | pd.Series:
    """
    Return DataFrame of historical factor of stock.

    Preconditions:
        - stock != ''
        - isinstance(stock, str)
    """
    url = f'https://www.macrotrends.net/stocks/charts/{stock}/'
    response = requests.get(url)
    new_url = str(response.url)

    links = ['pe-ratio', 'price-sales', 'price-book', 'net-worth', 'roe', 'roa', 'return-on-tangible-equity',
             'number-of-employees', 'current-ratio', 'quick-ratio', 'long-term-debt', 'total-liabilities',
             'debt-equity-ratio', 'roi', 'cash-on-hand', 'total-share-holder-equity', 'revenue', 'gross-profit',
             'net-income', 'shares-outstanding', 'stock-price-history']

    list_of_df = []
    for link in links:
        combined_link = str(new_url + link)
        list_of_df.append((link, get_one_data_from_link(combined_link)))
    return list_of_df
