import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import io
from sqlalchemy import create_engine
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

# --- Rest of your existing app code continues below ---
# --- SQL Engine ---
engine = create_engine('sqlite:///data.db')

# --- Your existing sidebar code ---
with st.sidebar:
    st.header("📥 Data Input")
    input_method = st.radio("Choose input method:", ["Upload CSV", "Enter Manually"])
    df = None

    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df = df.convert_dtypes()
            df.to_sql('user_data', con=engine, if_exists='replace', index=False)
            st.success("✅ File uploaded and saved to database.")

    elif input_method == "Enter Manually":
        sample_data = pd.DataFrame({
            "Category": ["A", "B", "A", "C"],
            "Value": [10, 20, 15, 5]
        })
        df = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)
        if not df.empty:
            df = df.convert_dtypes()
            df.to_sql('user_data', con=engine, if_exists='replace', index=False)
            st.success("✅ Manual data saved to database.")

# --- Continue with the rest of your existing app code ---
# ... [ALL YOUR EXISTING CODE AFTER THIS]

# --- Setup ---
st.set_page_config(page_title="Statistical Summary Generator", layout="wide")
st.title("📊 Statistical Summary Generator")
st.markdown("Upload a CSV or enter data manually. Run SQL queries, view advanced statistics, and download charts.")

# --- SQL Engine ---
engine = create_engine('sqlite:///data.db')

# --- Input Method ---
with st.sidebar:
    st.header("📥 Data Input")
    input_method = st.radio("Choose input method:", ["Upload CSV", "Enter Manually"])
    df = None

    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df = df.convert_dtypes()  # ✅ Fix for PyArrow serialization
            df.to_sql('user_data', con=engine, if_exists='replace', index=False)
            st.success("✅ File uploaded and saved to database.")

    elif input_method == "Enter Manually":
        sample_data = pd.DataFrame({
            "Category": ["A", "B", "A", "C"],
            "Value": [10, 20, 15, 5]
        })
        df = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)
        if not df.empty:
            df = df.convert_dtypes()  # ✅ Fix for PyArrow serialization
            df.to_sql('user_data', con=engine, if_exists='replace', index=False)
            st.success("✅ Manual data saved to database.")

# --- SQL Query ---
st.subheader("🧠 Run SQL Query")
query = st.text_area("Enter SQL query", "SELECT * FROM user_data")
if st.button("Run Query"):
    try:
        df = pd.read_sql_query(query, con=engine)
        df = df.convert_dtypes()  # ✅ Fix for PyArrow serialization
        st.success("✅ Query executed.")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")

# --- Analysis ---
if df is not None and not df.empty:
    st.subheader("📊 Data Preview")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # --- Tabs for Charts ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Summary", "Pie Chart", "Bar Graph", "Histogram", "Boxplot", "Heatmap"])

    with tab1:
        st.subheader("📈 Descriptive Statistics")
        summary = df.describe(include='all')
        st.dataframe(summary)
        csv = summary.to_csv().encode('utf-8')
        st.download_button("📥 Download Summary CSV", data=csv, file_name="summary.csv", mime="text/csv")

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
            pie_col = st.selectbox("Select column", categorical_cols, key="pie")
            pie_data = df[pie_col].value_counts()
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Distribution of '{pie_col}'")
            ax.axis('equal')
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Pie Chart", data=buf, file_name="pie_chart.png", mime="image/png")
        else:
            st.warning("⚠️ No categorical columns found.")

    with tab3:
        st.subheader("📶 Bar Graph")
        if categorical_cols:
            bar_col = st.selectbox("Select column", categorical_cols, key="bar")
            bar_data = df[bar_col].value_counts()
            fig, ax = plt.subplots()
            ax.bar(bar_data.index, bar_data.values, color='skyblue')
            ax.set_title(f"Frequency of '{bar_col}'")
            ax.set_xlabel(bar_col)
            ax.set_ylabel("Count")
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Bar Graph", data=buf, file_name="bar_graph.png", mime="image/png")
        else:
            st.warning("⚠️ No categorical columns found.")

    with tab4:
        st.subheader("📊 Histogram")
        if numeric_cols:
            hist_col = st.selectbox("Select column", numeric_cols, key="hist")
            fig, ax = plt.subplots()
            ax.hist(df[hist_col].dropna(), bins=10, color='orange', edgecolor='black')
            ax.set_title(f"Histogram of '{hist_col}'")
            ax.set_xlabel(hist_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📥 Download Histogram", data=buf, file_name="histogram.png", mime="image/png")
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
            st.download_button("📥 Download Boxplot", data=buf, file_name="boxplot.png", mime="image/png")
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
            st.download_button("📥 Download Heatmap", data=buf, file_name="heatmap.png", mime="image/png")
        else:
            st.warning("⚠️ No numeric columns found.")
else:

    st.info("👆 Upload a CSV or enter data manually to begin.")
