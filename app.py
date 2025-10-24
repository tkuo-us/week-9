import streamlit as st

from apputil import *


st.write(
'''
# Week 9: GroupEstimate - Part 1 Test

...
''')

# --- Test Section for Part 1 ---
st.subheader("Test GroupEstimate Initialization")

# user selects which estimate to test
option = st.selectbox("Select estimate type to test:", ["mean", "median", "invalid"])

try:
    gm = GroupEstimate(option)
    st.success(f"Successfully created GroupEstimate(estimate='{option}')")
    st.write(f"Stored estimate value: `{gm.estimate}`")

except Exception as e:
    st.error(f"Failed to create GroupEstimate: {e}")

# currently set for integer input
amount = st.number_input("Exercise Input: ", 
                         value=None, 
                         step=1, 
                         format="%d")

if amount is not None:
    st.write(f"The exercise input was {amount}.")

