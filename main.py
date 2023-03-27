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
import part1_factor_data_processing
import part2_recommendation_tree

# [1] Choosing the Main Influential Factors

# stocks = part1_factor_data_processing.read_csv()
stocks = ['MSFT', 'META', 'AAPL', 'GOOGL', 'SPY', 'SQQQ']
train_end_date = '2015-03-25'
stocks_performance = part1_factor_data_processing.get_percentage_growth_of_stocks(stocks, train_end_date)
top_ranked_stocks = part1_factor_data_processing.top_half(stocks_performance)
best_factors = part1_factor_data_processing.determining_best_factor(top_ranked_stocks)

# [2] Recommendation Tree
recommendation_tree = part2_recommendation_tree.create_recommendation_tree(best_factors, len(best_factors) - 1)

recommendation_tree.move_stock_to_subtree(('AAPL', {'pe-ratio': 0.4946519727984256, 'price-sales': 0.5835806630207975, 'price-book': 0.8104380119619405, 'roe': 0.8865666662667688, 'roa': 0.6767582349809744, 'return-on-tangible-equity': 0.8881634958214939, 'number-of-employees': 0.8474183005298309, 'current-ratio': -0.5958163812440904, 'quick-ratio': -0.6042497763708677, 'total-liabilities': 0.8647707467715722, 'debt-equity-ratio': 0.7765330213979921, 'roi': 0.4690201532614479, 'cash-on-hand': 0.8445638032474715, 'total-share-holder-equity': -0.08622598882515446, 'revenue': 0.8207153573825346, 'gross-profit': 0.7986135596428249, 'net-income': 0.784428847047673, 'shares-outstanding': -0.9291815200707428, 'average-price': 0.9796720015914931})
)



# Investment Simulation
# Visualization
