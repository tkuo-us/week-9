import streamlit as st

from apputil import *


st.write(
'''
# Week 9: GroupEstimate - Part 2 Test

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

# --- Test Section for Part 2 ---
option = st.selectbox("Select estimate type:", ["mean", "median"])
X = pd.DataFrame({
    "country": ["Brazil", "Brazil", "Kenya", "Kenya", "Ethiopia"],
    "roast": ["Light", "Dark", "Light", "Dark", "Light"]
})
y = pd.Series([90, 88, 85, 87, 92])

st.write("### Input Data")
st.dataframe(X)
st.write("### Ratings")
st.write(y)

# test fit()
if st.button("Run fit()"):
    try:
        gm = GroupEstimate(option)
        gm.fit(X, y)
        st.success(f"fit() completed using estimate='{option}'")
        st.dataframe(gm._group_stats.reset_index())
    except Exception as e:
        st.error(f"Error: {e}")

# currently set for integer input
amount = st.number_input("Exercise Input: ", 
                         value=None, 
                         step=1, 
                         format="%d")

if amount is not None:
    st.write(f"The exercise input was {amount}.")

