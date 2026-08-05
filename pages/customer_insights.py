import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from data import get_data, metric_card_style, custom_styled_df

st.title("👥 Customer Value & Behavior Analytics")
st.markdown("""
Comprehensive breakdown of consumer buying habits, purchasing frequency, and individual lifetime value (LTV). 
Use this diagnostic section to identify the highest-value accounts and optimize loyalty retention strategies.
""")

# metric column design using css
metric_card_style()

df = get_data()

#=====================================================================================================

# KPI Metrics

unique_cust = df['customer_id'].nunique()
avg_qty = df['quantity'].mean()
avg_spend_per_customer = df["total_spent"].sum() / unique_cust

col1, col2, col3 = st.columns(3)

col1.metric("Unique Customers", f"{unique_cust:,}")
col2.metric("Average Units Per Basket", f"{avg_qty:.1f}")
col3.metric("Average Spend Per Customer", f"${avg_spend_per_customer:.1f}")

# deep - dive analysis

st.markdown("### 📊 Customer Behavior & Purchase Insights")

with st.status("Analysis"):
    left_col , right_col = st.columns(2)

    with left_col:
        st.markdown("##### 🔍 Engagement Observations")
        st.markdown(
            f"""
            * **Active Customer Base:** The platform successfully engaged **{unique_cust:,}** 
            unique purchasing customers over this reporting period.

            * **Steady Transaction Volume:** Baskets maintain a consistent size with an average volume of **{avg_qty:.1f}
            units** per transaction.
            """
        )

    with right_col:
        st.markdown("##### 💡 Value Takeaways")
        st.markdown(
            f"""
            * **Customer Lifetime Value:** Individual customers yield a solid average spend profile of 
            **${avg_spend_per_customer:.2f}** across their interactions.

            * **Monetization Strategy:** Future campaigns should target increasing the units per basket 
            to efficiently scale the average customer value.
            """
        )

st.markdown(" --- ")

#=====================================================================================================

# Top Spenders Table

st.subheader("🔝 Top 10 High-Value Customers")
top_spenders = df.groupby('customer_id')['total_spent'].agg(['sum', 'count']).reset_index()

top_spenders.columns = ['customer_id', 'total_spent', 'visit_count']
top_spenders = top_spenders.sort_values(by='total_spent', ascending=False).reset_index(drop = True).head(10)

df1 = custom_styled_df(top_spenders, ["total_spent"], ["visit_count"])

st.dataframe(df1, use_container_width=True)

fig_top_cust = px.bar(
                top_spenders,
                x = "customer_id",
                y = "visit_count",
                title="Visit Frequency of Top 10 Spenders",
                labels={
                    "customer_id": "Customer ID",
                    "visit_count": "Total Visits"
                },
                color_discrete_sequence=['#60f252']

)

fig_top_cust.update_layout(
   
    title_x=0.5                 
)
st.plotly_chart(fig_top_cust)

#=====================================================================================================

# Customer loyalty : One-Time Buyers vs. Repeat Customers
# Custom colored underline with spacing
st.subheader("🤝 Customer loyalty : One-Time Buyers vs Repeat Customers")

cust_pur_count = df.groupby("customer_id")["total_spent"].count()

categories = np.select(
                  [cust_pur_count == 1, cust_pur_count == 2, cust_pur_count == 3, cust_pur_count >= 4],
                  ["1 purchase", "2 purchases", "3 purchases", "4+"],
                  default="Unknown"
)

count_labels = ["1 purchase", "2 purchases", "3 purchases", "4+"]

purc_counts = pd.Series(categories).value_counts().reindex(count_labels, fill_value=0)

pur_fig = px.bar(
    x = purc_counts.index,
    y = purc_counts.values,
    template='plotly_white'
)

pur_fig.update_layout(
    xaxis_title="Purchase Frequency Category",
    yaxis_title="Number of Customers",
    showlegend=False
)
col1, col2 = st.columns(2)
with col1:
  st.plotly_chart(pur_fig, use_container_width=True, key = "customer loyalty chart")
  
with col2:
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Calculating exact counts programmatically, so that the text never contradicts with the database updation
    one_to_three_count = purc_counts["1 purchase"] + purc_counts["2 purchases"] + purc_counts["3 purchases"]
    
    if one_to_three_count == 0:
        st.markdown("**Insight:** Customers with less than 4 purchases are exactly none. " \
        "That means they are extremely loyal to purchase 4+ times at our store.")
    else:
        st.markdown(f"**Insight:** You have **{purc_counts['4+']:,}** highly loyal repeat shoppers (4+ purchases),"
                    f" alongside **{one_to_three_count:,}** lower-frequency shoppers who could be targeted for retention campaigns.")


st.markdown("---")
#=====================================================================================================

# Customer spending Distribution

st.subheader("💰 Customer Spending Distribution")

customer_spending = (
        df.groupby("customer_id")["total_spent"]
        .sum()
        .reset_index()
)

# Histogram
fig = px.histogram(
        customer_spending,
        x="total_spent",
        nbins=10,
        title="Distribution of Customer Spending",
        labels={
            "Total Spent": "Total Spending",
            "count": "Number of Customers"
        },
        color_discrete_sequence=['#60f252']
)

fig.update_layout(
        xaxis_title="Total Spending",
        yaxis_title="Number of Customers",
        bargap=0.1,
        title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)
