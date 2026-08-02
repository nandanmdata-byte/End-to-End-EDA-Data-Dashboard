import streamlit as st
from data import get_data
import plotly.express as px

st.title("📦 Product Performance")

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

st.write("Here, we will have a look at the overall product sales and performance." )

df = get_data()

# KPI Metrics
#===================================================================================================================================

unique_items = df['item'].nunique()
max_price = df['price_per_unit'].max()

# Unique item , max price
col1, col2 = st.columns(2)
col1.metric("Unique Items Active", f"{unique_items}")
col2.metric("Max Item Price", f"${max_price:,.2f}")

st.markdown("---")

# Visualizations
#===================================================================================================================================

# Top Selling Quantities - bar chart
st.subheader("Top 5 Best Selling Items (by Quantity)")

top_items = df.groupby('item')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False).head(5)

fig_items = px.bar(
                top_items,
                x='item', 
                y='quantity', 
                color='quantity', 
                template='plotly_white')

st.plotly_chart(fig_items, use_container_width=True)

st.markdown("---")

#===================================================================================================================================

# Price vs Demand chart
st.subheader("Price vs. Quantity Demand")

fig_scatter = px.scatter(
                 df, 
                 x='price_per_unit', 
                 y='quantity', 
                 color='category', 
                 hover_data=['item'], 
                 opacity=0.6)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

#===================================================================================================================================

st.subheader("📦 Revenue Contribution by Product Category")
# Aggregate revenue by category
category_sales = (
    df.groupby("category", as_index=False)["total_spent"]
      .sum()
      .sort_values("total_spent", ascending=False)
)

# Create treemap
fig = px.treemap(
    category_sales,
    path=["category"],
    values="total_spent",
    color="total_spent",
    color_continuous_scale="Blues",
    title="Revenue Contribution by Product Category"
)

fig.update_traces(
    textinfo="label+value+percent root"
)

fig.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

# Display data table
st.dataframe(
    category_sales,
    use_container_width=True,
    hide_index=True
)