import streamlit as st

# Configure wide layout so your graphs look great
st.set_page_config(layout="wide")

side_head = st.sidebar.header(" 🛒 Retail Sales App")

# 1. Point directly to your newly moved files inside the views folder
home_page = st.Page("views/home.py", title="Home", icon="🏠", default=True)
data_summary = st.Page("views/data_summary.py", title="Data Summary", icon="📊")
sales_insights = st.Page("views/sales_insights.py", title = "Sales insights", icon = "🛒")
customer_insights = st.Page("views/customer_insights.py", title = "Customer insights", icon = "👤")
product_performance = st.Page("views/product_insights.py", title = "Product Metrics", icon = "📦")


# 2. Initialize the navigation menu
pg = st.navigation([home_page, data_summary, sales_insights, customer_insights, product_performance])

# 3. Render the selected page content
pg.run()

# 4. Bottom Index Navigation (Appears on every single page)
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Home", key="f_home", use_container_width=True):
        st.switch_page(home_page)
with col2:
    if st.button("📋 Data Summary", key="f_p2", use_container_width=True):
        st.switch_page(data_summary)
with col3:
    if st.button("📊 Sales Insights", key="f_sales", use_container_width=True):
        st.switch_page(sales_insights)
with col4:
    if st.button("🧑‍💼 Customer Insights", key="f_cust", use_container_width=True):
        st.switch_page(customer_insights)
with col5:
    if st.button("📊 Product Performance", key="f_prod", use_container_width=True):
        st.switch_page(product_performance)

