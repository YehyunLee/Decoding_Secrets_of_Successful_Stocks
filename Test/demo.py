# from yahoofinancials import YahooFinancials
# ticker = 'AAPL'
# yahoo_financials = YahooFinancials(ticker)
#
# # combine annual.
# all_statement_data_qt = yahoo_financials.get_financial_stmts('quarterly', ['income', 'cash', 'balance'], reformat=False)
# print(yahoo_financials.get_historical_price_data('2018-08-15', '2018-09-15', 'weekly'))
# # print(yahoo_financials.get_stock_earnings_data())
# # print(yahoo_financials.get_summary_data())
# # print(all_statement_data_qt)
# # get_daily_dividend_data
# # print(yahoo_financials.get_stock_profile_data())
#
# print(yahoo_financials.get_key_statistics_data())

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

pd.set_option('display.max_colwidth', 25)

# Input
symbol = input('Enter a ticker: ')
print('Getting data for ' + symbol + '...\n')

# Set up scraper
url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
html = soup(webpage, "html.parser")


def get_fundamentals():
    try:
        # Find fundamentals table
        fundamentals = pd.read_html(str(html), attrs={'class': 'snapshot-table2'})[0]

        # Clean up fundamentals dataframe
        fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        colOne = []
        colLength = len(fundamentals)
        for k in np.arange(0, colLength, 2):
            colOne.append(fundamentals[f'{k}'])
        attrs = pd.concat(colOne, ignore_index=True)

        colTwo = []
        colLength = len(fundamentals)
        for k in np.arange(1, colLength, 2):
            colTwo.append(fundamentals[f'{k}'])
        vals = pd.concat(colTwo, ignore_index=True)

        fundamentals = pd.DataFrame()
        fundamentals['Attributes'] = attrs
        fundamentals['Values'] = vals
        fundamentals = fundamentals.set_index('Attributes')
        return fundamentals

    except Exception as e:
        return e


def get_news():
    try:
        # Find news table
        news = pd.read_html(str(html), attrs={'class': 'fullview-news-outer'})[0]
        links = []
        for a in html.find_all('a', class_="tab-link-news"):
            links.append(a['href'])

        # Clean up news dataframe
        news.columns = ['Date', 'News Headline']
        news['Article Link'] = links
        news = news.set_index('Date')
        return news

    except Exception as e:
        return e


def get_insider():
    try:
        # Find insider table
        insider = pd.read_html(str(html), attrs={'class': 'body-table'})[0]

        # Clean up insider dataframe
        insider = insider.iloc[1:]
        insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)',
                           '# Shares Total', 'SEC Form 4']
        insider = insider[
            ['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total',
             'SEC Form 4']]
        insider = insider.set_index('Date')
        return insider

    except Exception as e:
        return e


print('Fundamental Ratios: ')
print(get_fundamentals())

print('\nRecent News: ')
print(get_news())

print('\nRecent Insider Trades: ')
print(get_insider())

print(print(get_fundamentals().to_string()))

# import finpie # or import finpie.fundamental_data

# default:
# source = 'macrotrends'
# freq = 'A'
# fd = finpie.Fundamentals('AAPL', source = 'macrotrends', freq = 'A')

# source options for financial statements and key metrics:
# 'yahoo', 'marketwatch', 'macrotrends'
# freq options:
# 'A', 'Q'

# default key metrics for marketwatch and macrotrends come from Finviz



# import numpy as np
# import pandas as pd
# import scipy
# import matplotlib.pyplot as plt
# data = pd.read_html()

# Share price / Earnings per share 20 ~25, 15 or lower, high pe is expesnsive, low cheap
# Market capitalization / Book value of equity 3 under or 1 udner
# diviend yeilds over 4% annual dividends per share / current share price
# ROE 15% 3 years increase
# 버핏은 이 ROE가 15% 이상으로 최근 3년 이내 꾸준히 증가하는 기업에 투자하라고 조언하기도 했습니다.
