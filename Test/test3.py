import pandas as pd

data = pd.read_html('https://www.macrotrends.net/stocks/charts/AAPL/apple/pe-ratio', skiprows=1)

df = pd.DataFrame(data[0])
df = pd.concat([df.columns.to_frame().T, df], ignore_index=True)
df.columns = range(len(df.columns))
df = df[1:]
df = df.rename(columns={0: 'Date', 1: 'Price', 2: 'EPS', 3: 'PE ratio'})
df['EPS'][1] = ''
df.set_index('Date', inplace=True)
df = df.sort_index()
df['trend'] = ''

#######################################################################################
# data = pd.read_html('https://www.macrotrends.net/stocks/charts/AAPL/apple/roe', skiprows=1)
#
# df = pd.DataFrame(data[0])
# df = pd.concat([df.columns.to_frame().T, df], ignore_index=True)
# df.columns = range(len(df.columns))
# # df = df[1:]
# # df = df.rename(columns={0: 'Date', 1: 'Price', 2: 'EPS', 3: 'PE ratio'})
# # df['EPS'][1] = ''
# # df.set_index('Date', inplace=True)
# # df = df.sort_index()
# # df['trend'] = ''
