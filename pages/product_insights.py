import streamlit as st
from data import get_data, metric_card_style, custom_styled_df
import plotly.express as px
import numpy as np

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
st.caption("Visual breakdown of the highest-volume products currently in stock.")

top_items = (
                df.groupby('item')['quantity']
                .sum()
                .reset_index()
                .sort_values(by='quantity', ascending=False)
                .head(5)
)

fig_items = px.bar(
                top_items,
                x='item', 
                y='quantity', 
                color='quantity', 
                template='plotly_white')

st.plotly_chart(fig_items, use_container_width=True)

st.info(
    """
    **Key Inventory Insights:**
    * 🚀 **Highest Volume Item:** `Item_2_Bev` leads inventory stock with approximately 690 units.
    * ⚖️ **Stable Categories:** Both `Food` items (`Item_14` and `Item_13`) show nearly equal quantities at roughly 625 units.
    * 📊 **Top 5 Threshold:** All five items shown maintain a high baseline of over 600 units each.
    """
)

st.markdown("---")

#===================================================================================================================================

st.subheader("📈 Price vs. Average Quantity Purchased")

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

# Analysis
st.markdown("##### Price Elasticity Analysis")

with st.container(border=True):
    st.markdown(f"###### 📌 Chart Legend ({selected_category})")
    
    col_legend_1, col_legend_2 = st.columns(2)
    with col_legend_1:
        st.markdown("- **X-Axis:** Price per Unit")
        st.markdown("- **Y-Axis:** Average Quantity Purchased")
    with col_legend_2:
        st.markdown(f"- **Bubble Identity:** Single unique product")
        st.markdown("- **Bubble Size:** Total volume of transactions")

# Dynamic Statistical Logic
correlation = summary["price_per_unit"].corr(summary["avg_quantity"])

# Unified Production Status Output
with st.status("📊 Statistical Interpretation Engine", expanded=True) as status:
    
    # Render the exact value so users can see the math
    st.metric(label="Calculated Correlation Coefficient (r)", value=f"{correlation:.2f}")
    st.markdown("---")
    
    if correlation >= 0.7:
        st.markdown("##### 🚀 Strong Positive Correlation")
        
        st.write("Prices and quantities move upwards together tightly. " \
        "Customers heavily favor high-tier premium options in large volumes.")
        status.update(label="Analysis: Strong Positive Trend", state="complete")
        
    elif 0.3 <= correlation < 0.7:
        st.markdown("##### 📈 Moderate Positive Correlation")

        st.write("The trendline shows a steady positive slope. " \
        "As prices increase, customers generally purchase larger quantities, " \
        "suggesting strong brand power or low price sensitivity.")
        status.update(label="Analysis: Moderate Positive Trend", state="complete")
        
    elif -0.3 < correlation < 0.3:
        st.markdown("##### ⚖️ Inelastic Demand (No Correlation)")

        st.write("The trendline is flat. " \
        "Purchasing volumes remain completely steady across all price fluctuations, " \
        "meaning price variations do not change customer buying habits.")
        status.update(label="Analysis: Stable Inelastic Trend", state="complete")
        
    elif -0.7 < correlation <= -0.3:
        st.markdown("##### 📉 Moderate Negative Correlation")

        st.write("Higher-priced items show a clear drop-off in order size. " \
        "Price sensitivity is active here; consider promotions or smaller packaging sizes.")
        status.update(label="Analysis: Moderate Negative Trend", state="complete")
        
    else:
        st.markdown("##### 🛑 Strong Negative Correlation")

        st.write("Classic price elasticity is present. Volume decays rapidly as prices rise. " \
        "High pricing strongly discourages larger customer baskets.")
        status.update(label="Analysis: Strong Negative Trend", state="complete")

st.markdown("---")


#===================================================================================================================================

# Revenuw Contribution by Product Category Tree Map

st.subheader("📦 Revenue Contribution by Product Category")

st.caption("Treemap analysis showcasing total revenue distribution "
"and percentage share across major product categories.")
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

#------------------------------------------------
# Analysis

# Metric columns 
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Highest Grossing Category", 
            value="Butchers", 
            delta="13% Share ($208,118)"
        )

    # Variance = Highest share - lowest share
    # Varince = 13% - 12%
    with col2:
        st.metric(
            label="Revenue Spread Variance", 
            value="Minimal (1%)", 
            delta="Balanced Portfolio"
        )
    with col3:
        st.metric(
            label="Lowest Core Category", 
            value="Milk Products", 
            delta="12% Share ($180,112)",
            delta_color="normal"
        )

# Deep-Dive Analysis
with st.container(border=True):
    st.markdown("### 📊 Key Treemap Insights")
    
    # Split into Data Observations and Strategic Actions
    left_analysis, right_actions = st.columns(2)
    
    with left_analysis:
        st.markdown("##### 🔍 Data Observations")
        st.markdown(
            """
            * **Uniform Revenue Distribution:** Revenue is exceptionally well-diversified. 
             Every single category seems to have an almost identical share of total sales,
               tightly bounded between **12% and 13%**.

            * **Leading Fresh & Tech Sectors:** `Butchers` (\$208.1k) and `Electric Household Essentials` (\$203.8k)
              lead the chart.

            * **Stable Baseline Floor:** Even the lowest-performing category visible (`Milk Products` at $180.1k) 
            stays highly competitive,
             remaining within 15% of the top-performing category.
            """
        )
        
    with right_actions:
        st.markdown("##### 💡 Strategic Recommendations")
        st.markdown(
            """
            * **Risk Mitigation Advantage:** Because no single category dominates the income stream, 
            the business is highly resilient against localized supply chain shocks or sudden category demand drops.

            * **Cross-Promotional Bundling:** Capitalize on this balanced engagement. 
            Create cross-category marketing bundles (e.g., pairing `Beverages` or `Food` with `Patisserie`) to increase overall basket size.

            * **Targeted Growth Incentives:** Since `Milk Products` and `Patisserie` lag slightly behind at 12%, 
            apply minor promotional pushes here to elevate them to the 13% benchmark.
            """
        )

st.markdown("###### * Above data in tabular form")
df1 = custom_styled_df(category_sales, ["total_spent"], [])
# Display data table
st.dataframe(
        df1, 
        use_container_width=True, 
        hide_index=True
)