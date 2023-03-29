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
import part3_investment_simulation
import plotly.express as px

if __name__ == '__main__':
    # [0] User Input
    # stocks = part1_factor_data_processing.read_csv()
    stocks = ['MSFT', 'META', 'AAPL', 'GOOGL', 'SPY', 'SQQQ']
    training_end_date = '2015-03-25'
    risk_percentage = 50

    # [1] Choosing the Main Influential Factors
    stocks_performance = part1_factor_data_processing.get_percentage_growth_of_stocks(stocks, training_end_date)
    top_ranked_stocks = part1_factor_data_processing.top_half(stocks_performance)
    best_factors = part1_factor_data_processing.determining_best_factor(top_ranked_stocks, training_end_date)

    # [2] Recommendation Tree
    recommendation_tree = part2_recommendation_tree.create_recommendation_tree(best_factors, len(best_factors) - 1)
    recommendation_tree.insert_stocks(stocks, training_end_date)
    buy_stocks = part2_recommendation_tree.determining_buy_stocks(recommendation_tree, risk_percentage)

    # [3] Investment Simulation
    # - '^IXIC' stands for NASDAQ
    # - '^GSPC' stands for S&P500

    # Benchmark
    benchmark_NASDAQ_simulation = part3_investment_simulation.benchmark_simulation('^IXIC', training_end_date)
    benchmark_S_and_P500_simulation = part3_investment_simulation.benchmark_simulation('^GSPC', training_end_date)
    benchmark_all_stocks_simulation = part3_investment_simulation.benchmark_simulation(stocks, training_end_date)

    # Using Statistically Significant Factors
    recommendation_tree_simulation = part3_investment_simulation.recommendation_tree_simulation(
        buy_stocks, training_end_date)

    # years = list(recommendation_tree_simulation.keys())
    # values = list(recommendation_tree_simulation.values())
    #
    # fig = px.line(x=years, y=values, labels={'x': 'Year', 'y': 'Return on Investment'}, title='Simulation Results')
    # fig.show()

    import plotly.graph_objs as go

    # assuming your simulation results are stored in dictionaries called 'benchmark_NASDAQ_simulation' and 'benchmark_S_and_P500_simulation'
    nasdaq_years = list(benchmark_NASDAQ_simulation.keys())
    nasdaq_values = list(benchmark_NASDAQ_simulation.values())

    sp500_years = list(benchmark_S_and_P500_simulation.keys())
    sp500_values = list(benchmark_S_and_P500_simulation.values())

    benchmark_all_stocks_simulation_years = list(benchmark_all_stocks_simulation.keys())
    benchmark_all_stocks_simulation_values = list(benchmark_all_stocks_simulation.values())

    recommendation_tree_simulation_years = list(recommendation_tree_simulation.keys())
    recommendation_tree_simulation_values = list(recommendation_tree_simulation.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nasdaq_years, y=nasdaq_values, name='NASDAQ'))
    fig.add_trace(go.Scatter(x=sp500_years, y=sp500_values, name='S&P 500'))
    fig.add_trace(go.Scatter(x=benchmark_all_stocks_simulation_years, y=benchmark_all_stocks_simulation_values,
                             name='All Stocks'))
    fig.add_trace(go.Scatter(x=recommendation_tree_simulation_years, y=recommendation_tree_simulation_values,
                             name='Recommendation Tree'))

    fig.update_layout(title='Simulation Results', xaxis_title='Year', yaxis_title='Return on Investment')
    fig.show()
    # Investment Simulation
    # Visualization
