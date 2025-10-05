import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import io
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# GOOGLE SEARCH CONSOLE VERIFICATION - MUST BE AT THE VERY TOP
# =============================================================================
st.markdown("""
<meta name="google-site-verification" content="tQsz8YFMyt6nnY2BlK_iHjerblTPaPADAo0PZ2OYbTo" />
""", unsafe_allow_html=True)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="StatVision Pro | Advanced Statistical Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS FOR PROFESSIONAL LOOK
# =============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HEADER SECTION
# =============================================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">📊 StatVision Pro</h1>', unsafe_allow_html=True)
    st.markdown("### Enterprise Statistical Analysis Platform")
    st.markdown("---")

# =============================================================================
# SIDEBAR - DATA INPUT
# =============================================================================
with st.sidebar:
    st.markdown("## 🔧 Data Management")
    st.markdown("---")
    
    input_method = st.radio(
        "**Data Input Method**",
        ["Upload CSV", "Enter Manually", "Sample Dataset"],
        key="input_method"
    )
    
    df = None
    
    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader(
            "📁 Upload CSV File",
            type=["csv"],
            help="Upload your dataset in CSV format",
            key="file_uploader"
        )
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                df = df.convert_dtypes()
                st.success(f"✅ Dataset loaded: {len(df)} rows × {len(df.columns)} columns")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                
    elif input_method == "Enter Manually":
        st.markdown("### ✍️ Manual Data Entry")
        
        default_data = {
            "Department": ["Sales", "Marketing", "IT", "Finance", "HR"],
            "Region": ["North", "South", "East", "West", "North"],
            "Revenue": [150000, 89000, 210000, 120000, 75000],
            "Employees": [45, 22, 18, 32, 15],
            "Satisfaction": [4.2, 4.7, 4.9, 4.1, 4.8],
            "Growth_Rate": [12.5, 8.3, 25.1, 9.8, 6.2]
        }
        
        df = st.data_editor(
            pd.DataFrame(default_data),
            num_rows="dynamic",
            use_container_width=True,
            height=400,
            key="data_editor"
        )
        if not df.empty:
            st.success("✅ Data ready for analysis")
            
    elif input_method == "Sample Dataset":
        dataset_choice = st.selectbox(
            "🎯 Choose Sample Dataset",
            ["Sales Performance", "Customer Analytics", "Financial Metrics"],
            key="dataset_choice"
        )
        
        if dataset_choice == "Sales Performance":
            df = pd.DataFrame({
                'Product': ['iPhone', 'MacBook', 'iPad', 'Watch', 'AirPods'],
                'Category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
                'Region': ['North', 'South', 'East', 'West', 'North'],
                'Sales_Units': [100, 40, 150, 80, 200],
                'Revenue': [50000, 80000, 30000, 20000, 15000],
                'Customer_Rating': [4.5, 4.7, 4.3, 4.6, 4.8]
            })
        elif dataset_choice == "Customer Analytics":
            df = pd.DataFrame({
                'Customer_ID': range(1, 51),
                'Age_Group': np.random.choice(['18-25', '26-35', '36-45', '46-55'], 50),
                'Annual_Income': np.random.normal(75000, 25000, 50),
                'Spending_Score': np.random.randint(1, 100, 50),
                'Loyalty_Years': np.random.exponential(3, 50)
            })
        elif dataset_choice == "Financial Metrics":
            df = pd.DataFrame({
                'Company': ['Tech Corp', 'Finance Ltd', 'Retail Inc', 'Manufacturing Co'],
                'Revenue_Millions': [150, 89, 210, 120],
                'Profit_Margin': [0.25, 0.18, 0.32, 0.15],
                'Employee_Count': [450, 220, 180, 320],
                'Market_Cap': [1500, 890, 2100, 1200]
            })
        
        if df is not None:
            st.success(f"✅ {dataset_choice} dataset loaded: {len(df)} rows")

# =============================================================================
# MAIN DASHBOARD
# =============================================================================
if df is not None and not df.empty:
    df = df.convert_dtypes()
    
    # EXECUTIVE METRICS
    st.markdown("## 📈 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Records", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        numeric_cols_count = len(df.select_dtypes(include='number').columns)
        st.metric("Numeric Columns", numeric_cols_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        categorical_cols_count = len(df.select_dtypes(include=['object', 'string']).columns)
        st.metric("Categorical Columns", categorical_cols_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        missing_vals = df.isnull().sum().sum()
        st.metric("Missing Values", missing_vals)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # MAIN ANALYSIS TABS
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 Data Explorer", 
        "📊 Descriptive Stats", 
        "📈 Visualization", 
        "🔍 Distribution", 
        "📦 Advanced Stats",
        "🔥 Correlation",
        "📤 Export"
    ])
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    
    with tab1:
        st.subheader("📋 Data Explorer")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Dataset Preview")
            st.dataframe(df, use_container_width=True, height=400)
        
        with col2:
            st.markdown("#### Data Structure")
            st.json({
                "Shape": f"{df.shape[0]} rows × {df.shape[1]} columns",
                "Column Types": df.dtypes.astype(str).to_dict(),
                "Missing Values": int(df.isnull().sum().sum())
            })
    
    with tab2:
        st.subheader("📊 Descriptive Statistics")
        
        if numeric_cols:
            st.markdown("#### Numerical Summary")
            desc_stats = df[numeric_cols].describe()
            st.dataframe(desc_stats.style.format("{:.2f}"), use_container_width=True)
        
        if categorical_cols:
            st.markdown("#### Categorical Summary")
            for col in categorical_cols[:3]:  # Show first 3 to avoid overflow
                value_counts = df[col].value_counts()
                st.write(f"**{col}:** {len(value_counts)} unique values")
                st.dataframe(value_counts.head(), use_container_width=True)
    
    with tab3:
        st.subheader("📈 Data Visualization")
        
        viz_type = st.selectbox(
            "Select Chart Type",
            ["Bar Chart", "Pie Chart", "Histogram", "Box Plot", "Scatter Plot"],
            key="viz_type"
        )
        
        if viz_type == "Bar Chart" and categorical_cols:
            bar_col = st.selectbox("Select categorical column", categorical_cols, key="bar_col")
            chart_data = df[bar_col].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(chart_data.index, chart_data.values, color='skyblue', edgecolor='black')
            ax.set_title(f"Frequency of {bar_col}")
            ax.set_xlabel(bar_col)
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
        elif viz_type == "Pie Chart" and categorical_cols:
            pie_col = st.selectbox("Select categorical column", categorical_cols, key="pie_col")
            pie_data = df[pie_col].value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
            ax.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', 
                  startangle=90, colors=colors)
            ax.set_title(f"Distribution of {pie_col}")
            st.pyplot(fig)
            
        elif viz_type == "Histogram" and numeric_cols:
            hist_col = st.selectbox("Select numeric column", numeric_cols, key="hist_col")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df[hist_col].dropna(), bins=15, color='lightcoral', 
                   edgecolor='black', alpha=0.7)
            ax.set_title(f"Distribution of {hist_col}")
            ax.set_xlabel(hist_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            
        elif viz_type == "Box Plot" and numeric_cols:
            fig, ax = plt.subplots(figsize=(10, 6))
            df[numeric_cols].boxplot(ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Box Plot of Numerical Variables")
            st.pyplot(fig)
            
        elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, key="scatter_y")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df[x_col], df[y_col], alpha=0.6)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} vs {x_col}")
            st.pyplot(fig)
    
    with tab4:
        st.subheader("🔍 Distribution Analysis")
        
        if numeric_cols:
            dist_col = st.selectbox("Select variable for analysis", numeric_cols, key="dist_col")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogram
                fig, ax = plt.subplots(figsize=(10, 6))
                data = df[dist_col].dropna()
                ax.hist(data, bins=15, alpha=0.7, color='lightblue', label='Histogram')
                ax.set_title(f"Distribution of {dist_col}")
                ax.set_xlabel(dist_col)
                ax.legend()
                st.pyplot(fig)
            
            with col2:
                # Basic statistics
                st.markdown("#### Distribution Statistics")
                stats_data = {
                    'Mean': data.mean(),
                    'Median': data.median(),
                    'Std Dev': data.std(),
                    'Skewness': stats.skew(data),
                    'Kurtosis': stats.kurtosis(data)
                }
                for stat, value in stats_data.items():
                    st.write(f"**{stat}:** {value:.4f}")
    
    with tab5:
        st.subheader("📦 Advanced Statistics")
        
        if numeric_cols:
            advanced_stats = pd.DataFrame(index=numeric_cols)
            
            for col in numeric_cols:
                data = df[col].dropna()
                advanced_stats.loc[col, 'Mean'] = data.mean()
                advanced_stats.loc[col, 'Median'] = data.median()
                advanced_stats.loc[col, 'Std Dev'] = data.std()
                advanced_stats.loc[col, 'Skewness'] = stats.skew(data)
                advanced_stats.loc[col, 'Kurtosis'] = stats.kurtosis(data)
                
                # T-test against mean
                t_stat, p_val = stats.ttest_1samp(data, data.mean())
                advanced_stats.loc[col, 'T-Statistic'] = t_stat
                advanced_stats.loc[col, 'P-Value'] = p_val
            
            st.dataframe(advanced_stats.style.format("{:.4f}"), use_container_width=True)
    
    with tab6:
        st.subheader("🔥 Correlation Analysis")
        
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, ax=ax, fmt='.2f')
            ax.set_title('Correlation Matrix Heatmap')
            st.pyplot(fig)
    
    with tab7:
        st.subheader("📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Data")
            
            # CSV Export (always works)
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                data=csv,
                file_name=f"statistical_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_csv"
            )
            
            # Simple Excel alternative without xlsxwriter
            try:
                # Try to create Excel with basic pandas
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    if numeric_cols:
                        df[numeric_cols].describe().to_excel(writer, sheet_name='Statistics')
                st.download_button(
                    "📥 Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"statistical_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel",
                    key="download_excel"
                )
            except Exception as e:
                st.info("📝 Excel export requires additional packages. CSV export is available.")
        
        with col2:
            st.markdown("#### Export Report")
            if st.button("📄 Generate Analysis Report", key="generate_report"):
                report = f"""
# Statistical Analysis Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Dataset:** {df.shape[0]} rows × {df.shape[1]} columns

## Summary Statistics
- Total Records: {len(df):,}
- Numeric Variables: {len(numeric_cols)}
- Categorical Variables: {len(categorical_cols)}
- Missing Values: {df.isnull().sum().sum()}

## Dataset Overview
{df.describe().to_string()}

Generated by StatVision Pro - Advanced Statistical Analysis Platform
                """
                st.download_button(
                    "📥 Download Report",
                    data=report,
                    file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    key="download_report"
                )

else:
    # WELCOME SCREEN
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem;'>
        <h1 style='font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🚀 Welcome to StatVision Pro
        </h1>
        <p style='font-size: 1.3rem; color: #666; margin-bottom: 3rem;'>
            The Ultimate Enterprise Statistical Analysis Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Advanced Features
        - **Multiple Data Input Methods**
        - **Comprehensive Statistics**
        - **Professional Visualizations**
        - **Distribution Analysis**
        - **Export Capabilities**
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Sample Analytics
        - **Sales Performance**
        - **Customer Analytics** 
        - **Financial Metrics**
        - **Research Data**
        """)

# =============================================================================
# SEO CONTENT FOR GOOGLE
# =============================================================================
st.markdown("---")
st.markdown("""
### 🔍 Free Online Statistical Analysis Tool

**StatVision Pro** - Professional statistical analysis platform for data scientists, researchers, and business analysts.

#### 📊 Features:
- Data Import & Manual Entry
- Statistical Analysis & Visualization  
- Distribution Analysis & Correlation
- Export Functionality & Reports

*100% Free - Professional Enterprise Platform - Google Verified*
""")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d;'>"
    "StatVision Pro © 2024 | Enterprise Statistical Analysis Platform"
    "</div>",
    unsafe_allow_html=True
)
