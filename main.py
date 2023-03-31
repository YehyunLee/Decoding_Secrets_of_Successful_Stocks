"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks

Instructions (READ THIS FIRST!)
===============================

1. All files must be at same level folder.
2. Install requirements.
3. Run this file. Website powered by Streamlit will pop up.
4. Choose options in website and click 'Run Program'.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""


if __name__ == '__main__':
    import sys
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", "part1_user_input_visualization.py"]
    sys.exit(stcli.main())

    # import doctest
    # doctest.testmod(verbose=True)
    #
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': [part2_factor_data_processing, part3_recommendation_tree, part4_investment_simulation],
    #     'allowed-io': ['main'],
    # })
