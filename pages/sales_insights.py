import streamlit as st
import pandas as pd
from data import get_data, metric_card_style, custom_styled_df
import plotly.express as px

st.title("📈 Sales Insights")

metric_card_style()

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
    st.subheader("💸 Revenue by Category")

    st.caption("Contribution of categories to the overall sales")

    cat_sales = (
                df.groupby('category')['total_spent']
                .sum()
                .reset_index()
                .sort_values(by='total_spent', ascending=True)
)
   
    
    fig_cat = px.bar(
                cat_sales, 
                x='total_spent', 
                y='category', 
                orientation='h', 
                template='plotly_white'
)
    
    st.plotly_chart(fig_cat, use_container_width=True)
    
    st.info("""
        **💡 Strategic Insight:** **Butchers** and **Electric Household Essentials** lead overall sales generation. 
        However, revenue distribution is highly balanced across the board; 
        our lowest-performing segment (**Milk Products**) still performs really well in comparison with the top categories. 
        """)
    
with col_right:
    st.subheader("💳 Revenue Share by Payment Method")
    st.caption("Distribution of total financial transaction volume across payment channels.")

    pay_sales = df.groupby('payment_method')['total_spent'].sum().reset_index()

    fig_pay = px.pie(
                pay_sales,
                values='total_spent', 
                names='payment_method', 
                hole=0.4, 
                template='plotly_white'
)
    
    st.plotly_chart(fig_pay, use_container_width=True)
    st.info("""
    **💡 Key Takeaway:** Cash remains the primary revenue driver at **34.6%**, 
    but non-cash digital channels (Digital Wallets and Credit Cards) 
    combined make up the vast majority (**65.4%**) of all transaction volumes. 
    """)

st.markdown("---")
#===================================================================================================================================

# Sales by Location

loc_sales = df.groupby("location")["total_spent"].sum().reset_index()

st.subheader("◔ Total Sales by Location")
st.caption("Distribution of total sales across in-store and online.")

fig_loc_sales = px.pie(
                loc_sales,
                values= "total_spent",
                names= "location",
                hole=0.4, 
                template= "plotly_white"
)

st.plotly_chart(fig_loc_sales, use_container_width=True)
st.info("""
    **💡 Summary:** Even though **online** platform leads in sales generation, 
    the data shows there is negligible difference between **in-store** and **online** total sales. 
    """)
st.markdown("---")
#=================================================================================================================================== 

# Monthly revenue trend

st.subheader("📈 Monthly Revenue Trend")
st.caption("Historical monthly sales performance from 2022 through late 2024 to identify seasonal macro trends.")

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

df["Year-Month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly_revenue = (
    df.groupby("Year-Month", as_index = False)["total_spent"].sum()
    )

# Removing last row since Jan 2025 data is incomplete
# Only for completed months
monthly_sales = monthly_revenue.iloc[:-1]

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

st.info("""
**💡 Strategic Insight:** Revenue demonstrates a highly resilient baseline, consistently averaging between **\$40k and $45k per month**. 
A distinct **bi-annual cyclical pattern** is visible, with major sales surges peaking every **January** and **July**, 
immediately followed by a sharp normalization phase the next month. 
""")

st.caption("The table below shows the monthly sales from Jan 1 2022 to Dec 31 2024.")

df1 = custom_styled_df(monthly_sales, ["total_spent"],[])

st.dataframe(df1, use_container_width=True, hide_index=True)

#===================================================================================================================================
