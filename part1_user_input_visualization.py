"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks (Part 1)

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""
from __future__ import annotations

import datetime
from datetime import timedelta

import plotly.graph_objs as go
import streamlit as st

# from python_ta.contracts import check_contracts

from PIL import Image  # Import image from pillow to open images

import part2_factor_data_processing
import part3_recommendation_tree
import part4_investment_simulation


# @check_contracts
def user_input() -> None:
    """
    This function runs the Streamlit library and opens up the browser. The purpose
    of Streamlit is to display statistics and also takes user input directly from the browser.
    This will also call run_program function as well as visualization function.
    """
    # Set Title of Web Page
    st.set_page_config(page_title="Decoding the Secrets of Successful Stocks")

    # Title
    st.title("Decoding the Secrets of Successful Stocks")

    st.text("Project by Yehyun Lee, Aung Zwe Maw and Wonjae Lee")
    st.text("Web page written and hosted by Yehyun Lee")
    # This un-indent is needed. Due to st.text reading function tab as indent of texts.
    st.text("""Copyright and Usage Information
===============================

This page is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This page is Copyright (c) 2023 Yehyun Lee.""")

    # Display Image
    img = Image.open("theme.png")
    st.image(img, width=400)
    url = "https://unsplash.com/@chrisliverani"
    st.markdown("*Image credit [Chris Liverani](%s)*" % url)

    # Header
    st.header("About")

    # Subheader
    st.subheader("Project Goal")

    # Text
    # Dev Note: "⠀" is a blank symbol to fix streamlit error not having tab in first sentence.
    st.write("""⠀\tAs an investor, the question is, which stocks are most profitable in the long-term, and what factors
    contribute to their success? Our team will use a tree data structure to identify the promising factors
    and the most likely companies to invest in and utilize the backtesting approach to determine the
    profitability of the investments.""")

    st.write("""⠀\tWe aim to determine the most promising stocks for investment by
    analyzing the correlation between their performance metrics. Based on the analysis, we will rank the stocks
    using a binary tree to group the stock by ranking for investment. We will then simulate backtesting results
    based on the conclusions drawn from the correlation analysis and historical data.""")

    # Subheader
    st.subheader("Motivation")

    # Text
    st.write("""⠀\tOne of the reasons for this project is the increase in interest in stocks during and after the 
    pandemic. Many people have turned to invest in stocks to make passive income or grow their savings during a time of
    economic uncertainty. However, with so many companies to choose from, it can be challenging to know which
    ones are most likely to provide a good return on investment. By using past datasets, we can analyze
    historical data, current market trends, and other relevant factors to identify the companies that are
    confused to perform well in the future. This can help investors make more informed ed decisions about where
    to put their money and maximize their returns. Another motivation for developing a stock market investment
    program is the passion of one of our partners, Yehyun Lee for stock market trends. His passion positively
    affected us and we were also willing to explore the trends along with him.""")

    url = "https://github.com/YehyunLee/CSC111-Project"
    st.write("For more information about our project, please visit [Yehyun's Github](%s) and check the LaTeX file"
             "." % url)

    # Header
    st.header("User Input")

    # Text
    st.write("Choose stocks that you might want to invest.")

    # Subheader
    st.subheader("Choosing Stocks")

    st.warning("Please select more than 2 stocks by precondition.")

    # Radio Button
    status1 = st.radio("Select Methods 👉", ('Select All (Recommended)', 'Options', 'Manual (Expert Only)'))
    stocks = part2_factor_data_processing.read_csv()

    if status1 == 'Select All (Recommended)':
        st.info("Selecting all takes around 5 minutes to run program.")
    elif status1 == 'Options':
        # Multi select box
        stocks = st.multiselect('Select Stocks', stocks)
    else:
        st.warning("We highly recommend you avoid using this option unless you are well aware of stocks that are "
                   "supported by APIs the program use. Some stocks may cause error. However, we've put internal work "
                   "to handle these issues. Give a shot! 🧪")
        stocks = st.text_input("Write in list[str] form", "['MSFT', 'META', 'AAPL', 'GOOGL', 'SQQQ']")
        stocks = [char.strip() for char in eval(stocks)]  # Remove spaces, re-format incorrect input.

    # Write the selected options
    st.write("You selected", len(stocks), 'stocks')
    st.success(stocks)

    # Subheader
    st.subheader("Choosing Date")

    st.info("Default value is recommended.")
    end_datetime = st.date_input(
        "When\'s you will like to start investing?",
        datetime.date(2016, 3, 25)) - timedelta(days=365)
    st.write('Program will train from 2009 to', end_datetime, 'and start investing', end_datetime + timedelta(days=365))
    end_date = str(end_datetime)

    # Subheader
    st.subheader("Choosing Risk Percentage")

    # Slider
    st.info("The program allocates its investments in a number of top-ranked stocks that corresponds "
            "to the given risk percentage. "
            "If risk percentage is 100%, program invest all stocks including bad performing stocks. "
            "If 10%, program invest top 10% of ranked stocks. "
            "A lower risk percentage leads to investment of fewer stocks but only top performing stocks. "
            "Default value is set to 50%.")
    risk_percent = st.slider("Select Risk Percentage (%)", 1, 100, value=50)

    # Print the risk_percent
    # format() is used to print value of a variable at a specific position
    st.text('Selected: {}%'.format(risk_percent))

    # Subheader
    st.subheader("Choosing Factors")

    st.warning("Choosing many factors cause significant increase of running time due to nature of Recommendation Tree!")

    # Radio Button
    status2 = st.radio("Select Factors 👉", ('Select All', 'Options (Recommended)'))
    st.info("The 'average-price' factor will be included as a minimum requirement.")
    factors_to_use = ['pe-ratio', 'price-sales', 'price-book', 'roe', 'roa', 'return-on-tangible-equity',
                      'number-of-employees', 'current-ratio', 'quick-ratio', 'total-liabilities',
                      'debt-equity-ratio', 'roi', 'cash-on-hand', 'total-share-holder-equity', 'revenue',
                      'gross-profit', 'net-income', 'shares-outstanding']

    if status2 == 'Options (Recommended)':
        # Multi select box
        factors_to_use = st.multiselect('Select Factors', factors_to_use)

    st.write("You selected", len(factors_to_use) + 1, 'factors')
    st.success(f"Factors selected: {factors_to_use + ['average-price']}")

    # Subheader
    st.subheader("Confirm User Input")
    st.warning("Please review your inputs and click 'Run Program' to confirm.")
    st.success(f"Stocks: {stocks}")
    st.success(f"Start Investing: {end_datetime + timedelta(days=365)}")
    st.success(f"Risk Percentage: {risk_percent}%")
    st.success(f"Factors: {factors_to_use + ['average-price']}")

    # Run Program
    if st.button('Run Program'):
        st.warning("Program is running...")
        st.info("Please wait while program is running. "
                "Running usually takes 5 ~ 10 minutes, but this depends on user inputs. "
                "If you click 'Run Program' again, it will re-run the program with updated options.")
        figure = run_program(stocks, end_date, risk_percent, factors_to_use)
        st.plotly_chart(figure[0])
        st.write("Statistics: ")
        st.success(f"Some stocks are not supported by APIs, thus, the program had to filter out the stocks. "
                   f"Here are stocks that were used to train the model: "
                   f"{figure[1]}")
        st.success("Here are ranked factors and their correlation values that were used to determine "
                   f"list of buy stocks: {figure[2]}")
        st.success("Here are list of stocks that program decided to invest: "
                   f"{figure[3]}")


# @check_contracts
def run_program(list_of_stocks: list[str], training_end_date: str, risk_percentage: int, factors: list[str]) -> \
        tuple[go.Figure, list[str], list[tuple[str, float]], list[str]]:
    """Runs the simulation and returns a graph showing the end results (brings information from part 2, 3 and 4)"""
    # [Part 2] Choosing the Main Influential Factors
    filter_stocks = part2_factor_data_processing.filter_stocks(list_of_stocks, training_end_date)
    stocks_performance = part2_factor_data_processing.get_percentage_growth_of_stocks(filter_stocks, training_end_date)
    top_ranked_stocks = part2_factor_data_processing.top_half(stocks_performance)
    best_factors = part2_factor_data_processing.determining_best_factor(top_ranked_stocks, training_end_date, factors)

    # [Part 3] Recommendation Tree
    recommendation_tree = part3_recommendation_tree.create_recommendation_tree(best_factors, len(best_factors) - 1)
    recommendation_tree.insert_stocks(filter_stocks, training_end_date, factors)
    buy_stocks = part3_recommendation_tree.determining_buy_stocks(recommendation_tree, risk_percentage)

    # [Part 4] Investment Simulation
    benchmark_nasdaq_simulation = part4_investment_simulation.benchmark_simulation('^IXIC', training_end_date)
    benchmark_s_and_p500_simulation = part4_investment_simulation.benchmark_simulation('^GSPC', training_end_date)
    benchmark_all_stocks_simulation = part4_investment_simulation.benchmark_simulation(filter_stocks, training_end_date)
    # Using Statistically Significant Factors
    recommendation_tree_simulation = part4_investment_simulation.recommendation_tree_simulation(
        buy_stocks, training_end_date)

    fig = visualization(benchmark_nasdaq_simulation, benchmark_s_and_p500_simulation,
                        benchmark_all_stocks_simulation,
                        recommendation_tree_simulation)
    return (fig, filter_stocks, best_factors, buy_stocks)


# @check_contracts
def visualization(benchmark_nasdaq_simulation: dict[int, float], benchmark_s_and_p500_simulation: dict[int, float],
                  benchmark_all_stocks_simulation: dict[int, float], recommendation_tree_simulation: dict[int, float]) \
        -> go.Figure:
    """
    The function takes dict[int, float] inputs and use them to make a figure data type. The function is used for making
    graph figure, meaning visualization is used for visual purpose.
    """
    nasdaq_years = list(benchmark_nasdaq_simulation.keys())
    nasdaq_values = list(benchmark_nasdaq_simulation.values())

    sp500_years = list(benchmark_s_and_p500_simulation.keys())
    sp500_values = list(benchmark_s_and_p500_simulation.values())

    benchmark_all_stocks_years = list(benchmark_all_stocks_simulation.keys())
    benchmark_all_stocks_values = list(benchmark_all_stocks_simulation.values())

    recommendation_tree_years = list(recommendation_tree_simulation.keys())
    recommendation_tree_values = list(recommendation_tree_simulation.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nasdaq_years, y=nasdaq_values, name='NASDAQ'))
    fig.add_trace(go.Scatter(x=sp500_years, y=sp500_values, name='S&P500'))
    fig.add_trace(go.Scatter(x=benchmark_all_stocks_years, y=benchmark_all_stocks_values,
                             name='All User Input Stocks'))
    fig.add_trace(go.Scatter(x=recommendation_tree_years, y=recommendation_tree_values,
                             name='Recommendation Tree Filtered Stocks'))

    fig.update_layout(title='Simulation Results', xaxis_title='Year', yaxis_title='Return on Investment (%)')
    # Try fig.show()
    return fig


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    #
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['part2_factor_data_processing', 'part3_recommendation_tree', 'part3_recommendation_tree',
    #                       'part4_investment_simulation', 'plotly.graph_objs', 'datetime', 'PIL', 'streamlit'],
    #     # the names (strs) of imported modules
    #     'allowed-io': ['user_input'],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120,
    #     'disable': ['trailing-whitespace', 'consider-using-f-string', 'too-many-statements', 'eval-used']
    #     # These disable options are all for streamlit limitation.
    #     # 'trailing-whitespace': First sentence cannot have tab. Thus, blank symbol is included, then tab is added.
    #     # 'consider-using-f-string': Markdown cannot have f string.
    #     # 'too-many-statements' and 'eval-used' is needed for perfectness of website.
    # })

    user_input()
