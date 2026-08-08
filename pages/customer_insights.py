import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

st.write(
    "This table displays a data analysis report identifying the top 10 highest-spending customers, " \
    "ranked in descending order by their total monetary value." \
)

top_spenders = df.groupby('customer_id')['total_spent'].agg(['sum', 'count']).reset_index()

top_spenders.columns = ['customer_id', 'total_spent', 'visit_count']
top_10_spenders = top_spenders.sort_values(by='total_spent', ascending=False).reset_index(drop = True).head(10)

df1 = custom_styled_df(top_10_spenders, ["total_spent"], ["visit_count"])

st.dataframe(df1, use_container_width=True)

# key metrics and core insights
with st.container(border = True):
    l_col, r_col = st.columns(2)

    with l_col:
        st.markdown("""
            ##### 📌Key Metrics Defined: 

            * **customer_id:** Unique identifier for each specific buyer.
            
            * **total_spent:** Cumulative total amount spent by the customer. 

            * **visit_count:** Total number of separate transactions or store visits.
            
        """)

    with r_col:
        st.markdown("""
            ##### 💡Core Insights:

            * **Top Performer:** `CUST_24` is the highest-value customer, generating $68,452.00 across 519 visits.
            * **High Frequency:** All top 10 customers are highly loyal, each visiting over 460 times.
            * **Tight Spend Range:** The revenue gap between the 1st and 10th customer is relatively small (less than $6,500).
        """)



#----------------------------------------------------------------------------
# line graph of customers showing total spent vs visit count

sort_spenders = top_spenders.sort_values(by="total_spent", ascending=False)

# 2. Create a subplot framework with a secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 3. Add the Spend Line (Primary Y-Axis)
fig.add_trace(
    go.Scatter(
        x=sort_spenders["customer_id"],
        y=sort_spenders["total_spent"],
        name="Total Spent ($)",
        mode="lines+markers",
        line=dict(color="blue", width=3),
    ),
    secondary_y=False,
)

# 4. Add the Visit Count Line (Secondary Y-Axis)
fig.add_trace(
    go.Scatter(
        x=sort_spenders["customer_id"],
        y=sort_spenders["visit_count"],
        name="Visit Count",
        mode="lines+markers",
        line=dict(color="orange", width=3, dash="dash"),
    ),
    secondary_y=True,
)

# 5. Set axis titles
fig.update_layout(title_text="Spend vs. Visit Frequency Trend")
fig.update_yaxes(title_text="<b>Total Spent ($)</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Visit Count</b>", secondary_y=True)

# Render in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### 💡 Final Analysis Takeaways")
st.write(
    "By comparing the table and the graph side by side, " \
    "it reveals that high spending is driven by relentless consistency rather than high-ticket individual purchases."
)
st.markdown(
    """
    * **Consistent Loyalty:**
    Even as total spend drops from \$68k to \$57k, visits never drop below 450.
    This proves that even the "lower" spenders in this top tier are just as deeply habituated 
    and loyal as the absolute top spenders.
    
    * **Identification of High-Value "Whales":**
    Look at `CUST_05` and `CUST_13`. They maintain a high total spend despite making fewer overall visits to the business.

    ___These are the high-efficiency premium buyers. They spend a massive amount per transaction.___
        
    * **Identification of Low-Margin "Bargain Hunters":**
    Look at `CUST_09` and `CUST_01`. Their visit counts spike massively upward, 
    but their blue spend line continues its steady downward trajectory.


    ___These customers visit business constantly but have very small basket sizes,
    likely buying lower-cost items or exclusively shopping during sales.___
    """
)

st.markdown(
    """
    #### 🛠️ Strategic Business Recommendations
    * **Tailor Loyalty Perks By Segment:** 
    Instead of offering generic rewards, 
    give transactional frequency rewards (e.g., "Visit 5 times get a free item") to bargain hunters, 
    and high-ticket percentage discounts to the premium "whales" to maximize their larger cart sizes.

    * **Audit the Drop-Off Zone:**
    Notice how after `CUST_14`, both spend and visit counts begin to drop off in tandem. 
    This represents a distinct behavior shift where customer habituation begins to break down.
    """
)


st.markdown("---")
#=====================================================================================================

# Customer spending Distribution
st.subheader("💰 Customer Spending Distribution")

st.write("The graph explains how customers are distributed into different categories based on thier total spendings.")
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
        labels={
            "total_spent": "Total Spending ($)"  
        },
        color_discrete_sequence=['#60f252']
)

fig.update_layout(
        xaxis_title="Total Spending ($)",
        yaxis_title="Number of Customers",
        bargap=0.1,
        template='plotly_white' 
)

# st.plotly_chart(fig, use_container_width=True, key="customer_spending_distribution")

col1, col2 = st.columns([2, 1]) # Allocates more width to the chart

with col1:
    st.plotly_chart(fig, use_container_width=True, key="customer_spending_distribution")

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Calculate top stats programmatically
    max_spender = customer_spending.loc[customer_spending['total_spent'].idxmax()]
    avg_spend = customer_spending['total_spent'].mean()
    
    st.markdown(f"**Key Spend Insights:**")
    st.markdown(f"* **Average Lifetime Spend:** ${avg_spend:,.2f} per customer.")
    st.markdown(f"* **Top VIP Customer:** `{max_spender['customer_id']}` has contributed a massive **${max_spender['total_spent']:,.2f}** in revenue!")
    st.markdown(" Among the 25 total customers, the vast majority (10 customers) fall squarely under the \$60k - $62k spending category. " \
                "While our top VIP customer pushes our mathematical average up, " \
                "our core revenue stability relies on this tightly clustered group of consistent," \
                " high-value mid-tier spenders.")
    