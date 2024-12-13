
import pandas as pd
import streamlit as st

st.header("Skyscrapers rank vs. Height")
df = pd.read_csv('skyscrapers(in).csv', index_col = 0)
df[["statistics.rank" , "statistics.height"]].plot.line(x = "statistics.rank" , y = "statistics.height")
