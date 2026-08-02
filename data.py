import streamlit as st
import pandas as pd

@st.cache_data
def get_data():
    # Streamlit loads this once and remembers it across all pages
    return pd.read_csv("retail_store_sales_clean.csv")
