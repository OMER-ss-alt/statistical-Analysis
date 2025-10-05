import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- GOOGLE VERIFICATION - MUST BE AT THE TOP ---
st.markdown("""
<meta name="google-site-verification" content="tQsz8YFMyt6nnY2BlK_iHjerblTPaPADAo0PZ2OYbTo" />
""", unsafe_allow_html=True)

# --- Simple Working App ---
st.set_page_config(
    page_title="Omer's Statistical Analysis Tool | Free Data Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Omer's Statistical Analysis Tool")
st.write("Free online statistical analysis and data visualization platform")

# Sample data that always works
sample_data = {
    'Product': ['iPhone', 'MacBook', 'iPad', 'Shoes', 'Shirts', 'Books'],
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Fashion', 'Fashion', 'Education'],
    'Region': ['North', 'South', 'East', 'West', 'North', 'South'],
    'Sales': [50000, 80000, 30000, 20000, 15000, 10000],
    'Units': [100, 40, 150, 300, 500, 800]
}

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'], key="uploader")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV file loaded successfully!")
else:
    df = pd.DataFrame(sample_data)
    st.info("📊 Using sample data. Upload a CSV file to use your own data.")

# Display data
st.subheader("📋 Data Preview")
st.dataframe(df)

# Manual column detection (GUARANTEED to work)
categorical_cols = []
numeric_cols = []

for col in df.columns:
    if df[col].dtype == 'object':  # Text columns
        categorical_cols.append(col)
    elif pd.api.types.is_numeric_dtype(df[col]):  # Number columns
        numeric_cols.append(col)

st.write(f"**📊 Categorical columns:** {categorical_cols}")
st.write(f"**📈 Numeric columns:** {numeric_cols}")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Pie Chart", "📈 Bar Chart", "📋 Summary"])

with tab1:
    st.subheader("🧁 Pie Chart")
    if categorical_cols:
        selected_col = st.selectbox("Choose column:", categorical_cols, key="pie_select")
        value_counts = df[selected_col].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Distribution of {selected_col}")
        st.pyplot(fig)
    else:
        st.error("No categorical columns found!")

with tab2:
    st.subheader("📈 Bar Chart")
    if categorical_cols:
        selected_col = st.selectbox("Choose column:", categorical_cols, key="bar_select")
        value_counts = df[selected_col].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(value_counts.index, value_counts.values, color='lightblue')
        ax.set_title(f"Frequency of {selected_col}")
        ax.set_xlabel(selected_col)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.error("No categorical columns found!")

with tab3:
    st.subheader("📋 Summary")
    st.write(df.describe())

# SEO Content
st.markdown("---")
st.markdown("""
### 🎯 Free Statistical Analysis Tool
**Omer's Statistical Analysis Tool** - Professional data analysis platform for students, researchers, and data analysts.

**Features:** CSV upload, Pie charts, Bar graphs, Data visualization, Statistical analysis
**100% Free** - No registration required - Works on all devices

*Perfect for academic research, business analysis, and scientific experiments.*
""")
