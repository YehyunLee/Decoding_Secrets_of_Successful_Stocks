import streamlit as st
import pandas as pd
import numpy as np

data = pd.DataFrame(
    np.random.randn(100, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(data)
# st.header('st.button')
#
# if st.button('Say hello'):
#      st.write('Why hello there')
# else:
#      st.write('Goodbye')

# import streamlit.cli as cli
#
# import sys
# sys.argv = ['0','run','myApp']
# name = "main"
#
# cli.main()



import subprocess
import os

process = subprocess.Popen(["streamlit", "run", os.path.join(
            'application', 'main', 'services', 'streamlit.py')])

