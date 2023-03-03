from yahoofinancials import YahooFinancials
ticker = 'AAPL'
yahoo_financials = YahooFinancials(ticker)

all_statement_data_qt = yahoo_financials.get_financial_stmts('quarterly', ['income', 'cash', 'balance'], reformat=False)
print(yahoo_financials.get_historical_price_data('2018-08-15', '2018-09-15', 'weekly'))
