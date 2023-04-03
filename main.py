"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks

Description
==============================================================
This module contains the code for opening part 1 which it
will run all the rest of codes. Due to Streamlit limitation,
we had to have a important codes in part 1 and have a seperate
file that runs part 1.

Instructions (READ THIS FIRST!)
==============================================================

1. All files must be at same level folder.
2. Install requirements.
3. Run this file. Website powered by Streamlit will pop up.
4. Choose options in website and click 'Run Program'.

Copyright and Usage Information
==============================================================

This file is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""
import sys
from streamlit.web import cli as stcli


if __name__ == '__main__':
    # By using sys, TA do not need to copy-paste command in their terminal.
    # This will automatically do the job for running Streamlit.
    # Part 1 will then run "Run Program" which calls for part 2, 3, 4.
    sys.argv = ["streamlit", "run", "part1_user_input_visualization.py"]
    sys.exit(stcli.main())
