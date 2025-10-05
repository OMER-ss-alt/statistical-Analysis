import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import io
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# --- Page Configuration ---
st.set_page_config(
    page_title="Statistical Analysis Dashboard | Free Data Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GOOGLE SEARCH CONSOLE VERIFICATION ---
st.markdown("""
<meta name="google-site-verification" content="tQsz8YFMyt6nnY2BlK_iHjerblTPaPADAo0PZ2OYbTo" />
""", unsafe_allow_html=True)

# --- SQL Engine ---
engine = create_engine('sqlite:///data.db')

# --- Input Method ---
with st.sidebar:
    st.header("📥 Data Input")
    input_method = st.radio("Choose input method:", 
                           ["Upload CSV", "Enter Manually"],
                           key="unique_input_method_123")
    
    df = None

    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", 
                                        type=["csv"],
                                        key="unique_csv_uploader_456")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df = df.convert_dtypes()
            df.to_sql('user_data', con=engine, if_exists='replace', index=False)
            st.success("✅ File uploaded and saved to database.")

    elif input_method == "Enter Manually":
        sample_data = pd.DataFrame({
            "Category": ["A", "B", "A", "C", "B"],
            "Value": [10, 20, 15, 5, 25],
            "Score": [85, 92, 78, 65, 88]
        })
        df = st.data_editor(sample_data, 
                           num_rows="dynamic", 
                           use_container_width=True,
                           key="unique_data_editor_789")
        if not df.empty:
            df = df.convert_dtypes()
            df.to_sql('user_data', con=engine, if_exists='replace', index=False)
            st.success("✅ Manual data saved to database.")

# --- Main App ---
st.title("📊 Statistical Summary Generator")
st.markdown("Upload a CSV or enter data manually. Run SQL queries, view advanced statistics, and download charts.")

# --- SQL Query ---
if df is not None:
    st.subheader("🧠 Run SQL Query")
    query = st.text_area("Enter SQL query", "SELECT * FROM user_data", key="unique_sql_query_101")
    if st.button("Run Query", key="unique_run_btn_202"):
        try:
            df_query = pd.read_sql_query(query, con=engine)
            df_query = df_query.convert_dtypes()
            st.success("✅ Query executed.")
            st.dataframe(df_query)
            df = df_query
        except Exception as e:
            st.error(f"❌ SQL Error: {e}")

# --- Analysis ---
if df is not None and not df.empty:
    st.subheader("📊 Data Preview")
    st.dataframe(df, use_container_width=True)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # --- Tabs for Charts ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Summary", "Pie Chart", "Bar Graph", "Histogram", "Boxplot", "Heatmap"
    ])

    with tab1:
        st.subheader("📈 Descriptive Statistics")
        summary = df.describe(include='all')
        st.dataframe(summary)
        csv = summary.to_csv().encode('utf-8')
        st.download_button("📥 Download Summary CSV", data=csv, file_name="summary.csv", 
                          mime="text/csv", key="unique_download_summary_303")

        st.subheader("📐 Advanced Stats")
        if numeric_cols:
            stats_df = pd.DataFrame(columns=["Skewness", "Kurtosis", "T-Statistic", "P-Value"])
            for col in numeric_cols:
                skew = df[col].skew()
                kurt = df[col].kurtosis()
                t_stat, p_val = stats.ttest_1samp(df[col].dropna(), df[col].mean())
                stats_df.loc[col] = [skew, kurt, t_stat, p_val]
            st.dataframe(stats_df)

    with tab2:
        st.subheader("🧁 Pie Chart")
        if categorical_cols:
            pie_col = st.selectbox("Select column", categorical_cols, key="unique_pie_select_404")
            pie_data = df[pie_col].value_counts()
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Distribution of '{pie_col}'")
            ax.axis('equal')
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Pie Chart", data=buf, file_name="pie_chart.png", 
                              mime="image/png", key="unique_download_pie_505")
        else:
            st.warning("⚠️ No categorical columns found.")

    with tab3:
        st.subheader("📶 Bar Graph")
        if categorical_cols:
            bar_col = st.selectbox("Select column", categorical_cols, key="unique_bar_select_606")
            bar_data = df[bar_col].value_counts()
            fig, ax = plt.subplots()
            ax.bar(bar_data.index, bar_data.values, color='skyblue')
            ax.set_title(f"Frequency of '{bar_col}'")
            ax.set_xlabel(bar_col)
            ax.set_ylabel("Count")
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Bar Graph", data=buf, file_name="bar_graph.png", 
                              mime="image/png", key="unique_download_bar_707")
        else:
            st.warning("⚠️ No categorical columns found.")

    with tab4:
        st.subheader("📊 Histogram")
        if numeric_cols:
            hist_col = st.selectbox("Select column", numeric_cols, key="unique_hist_select_808")
            fig, ax = plt.subplots()
            ax.hist(df[hist_col].dropna(), bins=10, color='orange', edgecolor='black')
            ax.set_title(f"Histogram of '{hist_col}'")
            ax.set_xlabel(hist_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Histogram", data=buf, file_name="histogram.png", 
                              mime="image/png", key="unique_download_hist_909")
        else:
            st.warning("⚠️ No numeric columns found.")

    with tab5:
        st.subheader("📦 Boxplot")
        if numeric_cols:
            fig, ax = plt.subplots()
            df.boxplot(column=numeric_cols, ax=ax)
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Boxplot", data=buf, file_name="boxplot.png", 
                              mime="image/png", key="unique_download_box_1010")
        else:
            st.warning("⚠️ No numeric columns found.")

    with tab6:
        st.subheader("🔥 Correlation Heatmap")
        if numeric_cols:
            fig, ax = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Heatmap", data=buf, file_name="heatmap.png", 
                              mime="image/png", key="unique_download_heat_1111")
        else:
            st.warning("⚠️ No numeric columns found.")
else:
    st.info("👆 Upload a CSV or enter data manually to begin.")

# --- SEO Content for Google ---
st.markdown("---")
st.markdown("""
### 🔍 Free Online Statistical Analysis Tool

**Statistical Analysis Dashboard** is a comprehensive web-based platform for data analysis, visualization, and statistical testing. Perfect for students, researchers, and data analysts.

#### 📊 Features:
- **Data Upload**: CSV file support
- **Statistical Tests**: Descriptive statistics, T-tests, correlation analysis
- **Data Visualization**: Charts, graphs, heatmaps, and plots
- **SQL Queries**: Run custom SQL on your data
- **Export Results**: Download charts and statistics

#### 🎯 Use Cases:
- Academic research and projects
- Business intelligence
- Scientific data analysis
- Quality control metrics
- Market research analysis

*100% Free - No registration required - Works on all devices*
""")
