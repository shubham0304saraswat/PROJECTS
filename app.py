import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

st.title('My first app')
st.write("Table:")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
st.write("Here is the Dataframe")
st.write(df)
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.write("Here is teh line chart")
st.line_chart(chart_data)               
