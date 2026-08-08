# End-to-End EDA Dashboard 📊

Welcome to the **Python End-to-End EDA Dashboard** project repository! This interactive Streamlit dashboard conducts comprehensive Exploratory Data Analysis (EDA) across Sales, Product, and Customer dimensions using Pandas and Numpy. Built to demonstrate a professional approach to data analytics, it features automated cleaning scripts, dynamic visualizations, and data-driven business insights.

---

## 📜 Project Requirements

### 🎯 Objective
* **Centralize Data:** Clean and preprocess raw retail sales data using **Pandas** and **NumPy** to create a reliable, analysis-ready dataset.
* **Exploratory Data Analysis (EDA):** Analyze customer demographics, purchasing behavior, and product performance through interactive visualizations and statistical insights.
* **Interactive Dashboard:** Build an intuitive Streamlit dashboard featuring KPIs, dynamic filters, and trends designed to drive informed business decisions.

### 🔍 Data Quality Assessment & Cleaning
Before generating insights, the raw dataset undergoes a rigorous quality assessment pipeline to resolve:
* Missing value imputation and duplicate record removal.
* Correction of data types (e.g., dates, categorical variables).
* Standardization of inconsistent categorical entries.
* Feature engineering for optimized visualization.

---

## 📂 Project Structure

```text
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
```

---

## 🛠️ Tech Stack & Tools

* **Programming Language:** Python
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Plotly Express
* **Dashboard Framework:** Streamlit
* **Development Environment:** VS Code / PyCharm
* **Version Control:** Git & GitHub
* **Dataset Source:** *Retail Sales: Dirty Data for Cleaning* by Ahmed Mehmoud (Kaggle)

---

## 🚀 Getting Started

Follow these steps to set up and run the dashboard locally:

### 1. Clone the Repository
```bash
git clone https://github.com/nandanmdata-byte/End-to-End-EDA-Data-Dashboard.git
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install streamlit pandas numpy plotly
```
*(Note: Install the core libraries that is required other than the above mentioned ones : `pip install 'library_name' `)*

### 4. Run the Dashboard
```bash
streamlit run app.py
```

---

## 👨‍💻 About Me

Hello! I'm **Nandan M**, an **M.Sc. Physics graduate** transitioning into **Data Science**. I am currently completing a Data Science internship at Luminar Technolab in Kochi, Kerala, India. 

My background in physics has deeply sharpened my analytical thinking, quantitative problem-solving abilities, and passion for extracting structural, meaningful insights from complex systems. This project serves as a showcase of my technical skills in data pipeline engineering, statistical visualization, and interactive dashboard development.

🌐 **Connect with me:** [LinkedIn Profile](https://www.linkedin.com/in/nandan-m-ds/)

---

## 📄 License

This project is licensed under the [MIT License](https://github.com/nandanmdata-byte/End-to-End-EDA-Data-Dashboard/blob/main/LICENSE). You are free to use, modify, and distribute this project for personal or commercial purposes.
