import streamlit as st
import pandas as pd

@st.cache_data
def get_data():
    # Load dataset across all pages
    return pd.read_csv("datasets/clean_datasets/retail_store_sales_clean.csv")


def metric_card_style():
    
    st.markdown("""
    <style>
    /* Style every metric card container */
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Style the metric label text */
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #495057;
    }
    </style>
""", unsafe_allow_html=True)


def custom_styled_df(df1, currency_col, count_col):

    styler = df1.style.set_properties(**{
        'background-color': "#2A4C82", 
        'color': '#F8FAFC',             
        'border': '1px solid #475569',  
        'text-align': 'center'          
    })

    # a dictionary to capture the columns to format
    format_dict = {}

    # currency column format
    for col in currency_col:
        if col in df1.columns:
            format_dict[col] = "${:,.2f}"

    # count column format
    for colm in count_col:
        if colm in df1.columns:
            format_dict[colm] = "{:,.0f}"     
    return styler.format(format_dict)


