import pandas_datareader as web
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import yfinance as yf

start = dt.datetime(2018,1,1)
end = dt.datetime.now()

tickers = ['AAPL', 'META', 'GS', 'NVDA', 'SQQQ', '^IXIC']
colnames = []

adj_close = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start=start, end=end)
    adj_close = adj_close.join(data['Adj Close'], rsuffix=ticker)
    if len(colnames) == 0:
        combined = data[['Adj Close']].copy()
    else:
        combined = combined.join(data['Adj Close'])
    colnames.append(ticker)
    combined.columns = colnames

f1 = plt.figure(1)
plt.hist
plt.yscale('log')
for ticker in tickers:
    plt.plot(combined[ticker], label=ticker)
plt.legend(loc='upper right')
f1.show

f2 = plt.figure(2)
plt.hist
corr_data = combined.pct_change().corr(method='pearson')
sns.heatmap(corr_data, annot=True, cmap='coolwarm')
f2.show()
