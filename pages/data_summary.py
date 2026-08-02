import streamlit as st
from data import get_data

st.title("📋 Data Summary")

st.markdown("---")

# To highlight the metric containers
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

# Fetch instantly from RAM cache
df = get_data()

st.subheader("📊 Cleaned Data Dashboard Hub")

st.write(
    """
    This page provides a quick overview of the cleaned retail sales dataset.
    Before exploring the visualizations, you can review the dataset structure,
    summary statistics, and overall data quality.
    """
)

#=====================================================================================================================

_rows, _columns = df.shape

st.write("### 📌 Dataset Overview")

st.write(
    "The following metrics summarize the size of the dataset used throughout this dashboard."
)

col1, col2 = st.columns(2)

col1.metric("Total Records Loaded", _rows)
col2.metric("Total Columns Loaded", _columns)

st.text("")
st.markdown("---")

#=====================================================================================================================

st.text("")
st.text("")

st.write("### 👀 Dataset Preview")

st.write(
    "The table below displays the first **10 records** of the cleaned dataset, "
    "allowing you to verify the data after preprocessing."
)

st.dataframe(df.head(10))

st.markdown("---")

#=====================================================================================================================

st.write("### 📈 Summary Statistics")

st.write(
    "The statistical summary provides key descriptive measures such as "
    "**count, mean, standard deviation, minimum, maximum, and quartiles** "
    "for the numerical columns."
)

st.dataframe(df.describe())

st.markdown("---")

#=====================================================================================================================

st.write("### 🔍 Missing Values Check")

st.write(
    "A final validation is performed to confirm that the cleaned dataset "
    "contains no remaining missing values before analysis."
)

# Convert the missing values series into a DataFrame
missing_data = df.isnull().sum().reset_index()

missing_data.columns = ['Column', 'Count']

# Display clean table in Streamlit
st.dataframe(missing_data, use_container_width=True)

st.markdown("---")