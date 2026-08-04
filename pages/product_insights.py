import streamlit as st
from data import get_data, metric_card_style, custom_styled_df
import plotly.express as px

st.title("📦 Product Performance")

metric_card_style()

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

st.subheader("Price vs. Average Quantity Purchased")

# Category selector
categories = sorted(df["category"].unique())

selected_category = st.selectbox(
    "Select a Category",
    categories
)

# Filter data
filtered_df = df[df["category"] == selected_category]


summary = (
    filtered_df
    .groupby("price_per_unit", as_index=False)
    .agg(
        avg_quantity=("quantity", "mean"),
        transactions=("quantity", "count")
    )
)

fig = px.scatter(
        summary,
        x="price_per_unit",
        y="avg_quantity",
        size="transactions",   # Bubble size
        hover_name="price_per_unit",
        hover_data={
            "transactions": True,
            "avg_quantity": ":.2f",
            "price_per_unit": False
        },
        trendline="ols",
        trendline_color_override="red",
        title=f"Price vs Average Quantity Purchased - {selected_category}"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Price per Unit ($)",
    yaxis_title="Average Quantity Purchased",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Bubble size represents the number of transactions at each price level."
)

st.markdown("---")

#===================================================================================================================================

# Revenuw Contribution by Product Category Tree Map

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

df1 = custom_styled_df(category_sales, ["total_spent"], [])
# Display data table
st.dataframe(
        df1, 
        use_container_width=True, 
        hide_index=True
)