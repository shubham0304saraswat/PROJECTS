import streamlit as st
import pandas as pd

Heading = st.title('COduMinati')
name = st.text_input('Enter your name')
age = st.slider('Enter your age', 0, 100, 25)
options = ['Python', 'Java', 'C++', 'Ruby', 'JavaScript']
primary_lang = st.selectbox('Primary Language: ', options)
secondary_lang = st.selectbox('Secondary Language: ', options)
submit_flag = st.button('Submit')

df = pd.DataFrame({
    'Name': [name],
    'Age': [age],
    'Primary Language': [primary_lang],
    'Secondary Language': [secondary_lang]
})

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")   

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

if name and submit_flag:
    st.write(df) 