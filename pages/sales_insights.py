import streamlit as st
import pandas as pd
from data import get_data
import plotly.express as px

st.title("📈 Sales Insights")


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


st.write("Here, we will have a look at the overall sales insights and impacts.")

df = get_data()

# KPI Metrics
total_rev = df['total_spent'].sum()
total_tx = df['transaction_id'].nunique()
aov = df['total_spent'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_rev:,.2f}")
col2.metric("Total Transactions", f"{total_tx:,}")
col3.metric("Average Order Value", f"${aov:,.2f}")


st.markdown("---")

#===================================================================================================================================

# Visualizations

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Category")
    cat_sales = df.groupby('category')['total_spent'].sum().reset_index().sort_values(by='total_spent', ascending=True)
    fig_cat = px.bar(cat_sales, x='total_spent', y='category', orientation='h', template='plotly_white')
    st.plotly_chart(fig_cat, use_container_width=True)
    
with col_right:
    st.subheader("Payment Method Split")
    pay_sales = df.groupby('payment_method')['total_spent'].sum().reset_index()
    fig_pay = px.pie(pay_sales, values='total_spent', names='payment_method', hole=0.4, template='plotly_white')
    st.plotly_chart(fig_pay, use_container_width=True)

st.markdown("---")

#=================================================================================================================================== 

# Monthly revenue trend

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

df["Year-Month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly_revenue = (
    df.groupby("Year-Month", as_index = False)["total_spent"].sum()
    )

# Removing last row since Jan 2025 data is incomplete
# Only for completed months
monthly_sales = monthly_revenue.iloc[:-1]

st.subheader("📈 Monthly Revenue Trend")

line_fig = px.line(
    monthly_sales,
    x = "Year-Month",
    y = "total_spent",
    markers=True,
    title="Monthly Revenue Trend"
)

line_fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue",
    title_x=0.5,
    hovermode="x unified"
)

line_fig.update_traces(
    line=dict(width=2),
    marker=dict(size=6)
)

st.plotly_chart(line_fig, use_container_width=True)

# Optional: Show monthly revenue table
st.dataframe(monthly_sales, use_container_width=True, hide_index=True)

#===================================================================================================================================
