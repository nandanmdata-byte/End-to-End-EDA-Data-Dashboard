
import streamlit as st
import pandas as pd
from PIL import Image
from data import get_data


image = Image.open("assets/13744794_Mar-Business_2.jpg")

st.image(image, width=400)

st.title("🏠 Retail Sales Web App 📊")

st.markdown("""Welcome!

This web application was developed using Streamlit as part of my **End-to-End EDA Dashboard** project. 
It presents a comprehensive exploratory data analysis (EDA) of a retail store sales dataset, 
highlighting key business insights through interactive visualizations and reports.

The raw dataset was cleaned and preprocessed using **Pandas**, **NumPy**, 
and other Python libraries to ensure high data quality before analysis.
Explore the dashboard below to discover customer trends, product performance, sales patterns, and other valuable insights.""")

st.markdown("*Note: Use the sidebar or navigation bar at the end of page, to jump to the next content*")

#=====================================================================================================================

#About section

expanded_bar = st.expander("About")
expanded_bar.markdown(""" 
* **Python libraries:** pandas, numpy, streamlit, PIL
* **Raw data source:** [*Retail Sales: Dirty Data for Cleaning* by Ahmed Mehmoud (Kaggle)](https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning)                   
* **Github link:** [End_to-End-EDA_Dashboard](https://github.com/nandanmdata-byte/End-to-End-EDA-Data-Dashboard.git)
* *Note: The data used for reporting is a cleaned version of above raw data* """)


#=====================================================================================================================

# Project Requirements

st.markdown("---")

st.markdown(
    "<div style='text-align: left; font-size: 28px; font-weight: bold;'>📜 <u>Project Requirements</u></div>",
    unsafe_allow_html=True
)

st.text("")

st.markdown(
    "<div style='text-align: left; font-size: 22px; font-weight: bold; margin-bottom: 10px;'>Objective</div>",
    unsafe_allow_html=True
)

st.markdown("""
* **Centralize data:** Clean and preprocess the raw retail sales CSV dataset using **Pandas**, **NumPy**,
 and other Python libraries to create a reliable, analysis-ready dataset.

* **Exploratory Data Analysis (EDA):** Analyze customer demographics, purchasing behavior,
 and product performance through interactive visualizations and statistical insights.

* **Interactive Dashboard:** Build an intuitive Streamlit dashboard with KPIs, filters,
 and visualizations to explore sales trends, customer demographics, and product performance.
""")

#=====================================================================================================================

# Technical Specifications

st.markdown("---")

st.markdown(
    "<div style='text-align: left; font-size: 28px; font-weight: bold;'>⚙️ <u>Technical Specifications</u></div>",
    unsafe_allow_html=True
)

st.text("")

st.markdown(
    "<div style='text-align: left; font-size: 22px; font-weight: bold;'>Data Source</div>",
    unsafe_allow_html=True
)

st.markdown("""
- **Dataset:** *Retail Sales: Dirty Data for Cleaning* by Ahmed Mehmoud (Kaggle)
- **Input Format:** CSV
- **Processing Libraries:** Pandas and NumPy
""")

st.markdown(
    "<div style='text-align: left; font-size: 22px; font-weight: bold;'>Data Quality Assessment</div>",
    unsafe_allow_html=True
)

st.markdown("""
Before analysis, the dataset undergoes a comprehensive quality assessment to identify and resolve:
- Missing values
- Duplicate records
- Invalid or inconsistent entries
- Incorrect data types
- Data formatting issues
""")

st.markdown(
    "<div style='text-align: left; font-size: 22px; font-weight: bold;'>Data Cleaning & Preparation</div>",
    unsafe_allow_html=True
)

st.markdown("""
The raw dataset is cleaned and transformed into an analysis-ready dataset by:
- Handling missing values
- Removing invalid records
- Correcting data types
- Standardizing categorical values
- Preparing features for visualization and analysis
""")

st.markdown(
    "<div style='text-align: left; font-size: 22px; font-weight: bold;'>Exploratory Data Analysis (EDA)</div>",
    unsafe_allow_html=True
)

st.markdown("""
Interactive visualizations are created to uncover business insights, including:
- Customer demographics
- Product performance
- Sales distribution
- Revenue trends
- Purchasing behavior
- Key business KPIs
""")

#=====================================================================================================================

# Project Structure

st.markdown("---")

st.markdown(
    "<div style='text-align: left; font-size: 28px; font-weight: bold;'>📂 <u>Project Structure</u></div>",
    unsafe_allow_html=True
)

st.code("""
End-to-End_EDA_Dashboard/
│
├── datasets/                 # Project data storage
│   ├── raw_datasets/         # Original, unmodified Kaggle data
│   └── clean_datasets/       # Processed, analysis-ready data
│
├── scripts/                  # Automated data cleaning Python scripts
├── docs/                     # Project documentation & deep dives
├── pages/                    # Multi-page Streamlit views
├── assets/                   # Images, banners, and icons
│
├── data.py                   # Centralized clean data access layer
├── app.py                    # Main Streamlit application entry point
├── LICENSE                   # MIT License
└── README.md                 # Project overview
""", language="text")

#=====================================================================================================================

# Tech Stack & Tools

st.markdown("---")

st.markdown(
    "<div style='text-align: left; font-size: 28px; font-weight: bold;'>🛠️ <u>Tech Stack & Tools</u></div>",
    unsafe_allow_html=True
)

st.markdown("""
- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Data Visualization:** Plotly Express
- **Dashboard Framework:** Streamlit
- **Development Environment:** VS Code, Pycharm
- **Version Control:** Git & GitHub
- **Research & Documentation:** Kaggle, Python Documentation, [discuss streamlit](https://discuss.streamlit.io/) and Google
""")

#=====================================================================================================================

# About Me

st.markdown("---")

st.markdown(
    "<div style='text-align: left; font-size: 28px; font-weight: bold;'>👨‍💻 <u>About Me</u></div>",
    unsafe_allow_html=True
)

st.markdown("""
Hello! I'm **Nandan M**, an **M.Sc. Physics graduate** transitioning into **Data Science**. 
I am currently doing a data science internship at Luminar Technolab Kochi, Kerala, India. 
My background in physics has strengthened my analytical thinking, problem-solving abilities, and passion for extracting meaningful insights from data.

This project demonstrates my skills in **data cleaning**,
 **exploratory data analysis (EDA)**, **data visualization**, and **interactive dashboard development** using Python and Streamlit.

**My linkedIn profile:** [LinkedIn Profile](https://www.linkedin.com/in/nandan-m-ds/)
""")

#=====================================================================================================================

# License

st.markdown("---")

st.markdown(
    "<div style='text-align: left; font-size: 28px; font-weight: bold;'>📄 <u>License</u></div>",
    unsafe_allow_html=True
)

st.markdown("""
This project is licensed under the [**MIT License**](https://github.com/nandanmdata-byte/End-to-End-EDA-Data-Dashboard/blob/main/LICENSE)

You are free to use, modify, and distribute this project for personal or commercial purposes in accordance with the terms of the license.
""")

#=====================================================================================================================

st.markdown("<br><br>", unsafe_allow_html= True)
st.markdown(
    "<div style='text-align: center; font-size: 28px; font-weight: bold;'>🫶 Thank you for visiting</div>",
    unsafe_allow_html=True
)
st.markdown("<br><br>", unsafe_allow_html= True)
#=====================================================================================================================

