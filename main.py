"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks

Instructions (READ THIS FIRST!)
===============================

...

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""
import part1_data

# Choosing the Main Influential Factors
# stocks = part1_data.read_csv()
stocks = ['MSFT', 'META', 'AAPL', 'GOOGL', 'SPY', 'SQQQ']
train_end_date = '2015-03-25'
stocks_performance = part1_data.get_percentage_growth_of_stocks(stocks, train_end_date)
top_ranked_stocks = part1_data.top_half(stocks_performance)

# c = create_game_tree([('f3', 3), ('f2', 2), ('f1', 1)], 2)

lst_of_dict = []
for top_stock in top_ranked_stocks:
    lst_of_dict.append(part1_data.all_factors_correlation(top_stock[0]))

average_factor_correlation = {}
for factor in lst_of_dict[0].keys():
    combined_tuple = tuple(each_top_stock[factor] for each_top_stock in lst_of_dict)
    average_factor_correlation[factor] = sum(combined_tuple) / len(combined_tuple)

# Recommendation Tree
# Investment Simulation
# Visualization
