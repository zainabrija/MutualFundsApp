import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import re
import time
import json
import os
import base64

# Set page config
st.set_page_config(
    page_title="Pakistan Mutual Funds Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 100%);
    }
    
    /* Top Navigation Bar */
    [data-testid="stToolbar"] {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%) !important;
        padding: 1rem 2rem;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
        height: auto !important;
    }

    /* Hide default sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Navigation container */
    .nav-container {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
        padding: 1rem;
        margin-bottom: 2rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .nav-container .stSelectbox {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.5rem;
    }

    .nav-container .stSelectbox > div > div {
        background: transparent !important;
        color: white !important;
    }

    /* Adjust main content padding for top nav */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* Main content area styling */
    .main {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 2rem;
        border-radius: 10px;
        color: #1e3a8a;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
        padding: 2rem 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar text and elements */
    .css-1d391kg .stSelectbox label {
        color: white !important;
    }
    
    .css-1d391kg p {
        color: #e0f2fe !important;
    }
    
    .css-1d391kg h3 {
        color: white !important;
        border-bottom: 2px solid #60a5fa;
    }
    
    /* Headers styling */
    h1 {
        color: #1e3a8a;
        font-size: 2.75rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        text-align: center;
        padding: 1.75rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    h2 {
        color: #1e3a8a;
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
    }
    
    h3 {
        color: #1e3a8a;
        font-size: 1.75rem !important;
        margin-top: 1.5rem !important;
        padding: 0.75rem 0;
        border-bottom: 2px solid #60a5fa;
    }
    
    /* Custom card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1.75rem;
        margin: 1.25rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.2);
        color: #1e3a8a;
        backdrop-filter: blur(10px);
    }
    
    /* Metric card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.2);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 1);
    }
    
    .metric-card h4 {
        color: #3b82f6;
        font-size: 1.1rem !important;
        margin: 0;
        font-weight: 500;
    }
    
    .metric-card p {
        color: #1e3a8a !important;
        font-size: 1.5rem !important;
        font-weight: 600;
        margin: 0.75rem 0 0 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%) !important;
        color: white !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Chart container styling */
    .chart-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1.75rem;
        margin: 1.25rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* DataFrame styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #1e3a8a !important;
    }
    
    .dataframe th {
        background: rgba(96, 165, 250, 0.1) !important;
        color: #1e3a8a !important;
    }
    
    .dataframe td {
        color: #1e3a8a !important;
    }
    
    /* Selectbox styling */
    .stSelectbox {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    /* Success/Info/Warning message styling */
    .stSuccess, .stInfo, .stWarning {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #1e3a8a !important;
        border: 1px solid rgba(96, 165, 250, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Text color overrides */
    p {
        color: #1e3a8a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Cache configuration
CACHE_FILE = "mutual_funds_cache.json"
CACHE_DURATION = 3600  # 1 hour in seconds

def load_cached_data():
    """Load cached data if it exists and is not expired"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                if time.time() - cache_data['timestamp'] < CACHE_DURATION:
                    return pd.DataFrame(cache_data['data'])
        except Exception as e:
            st.warning(f"Error loading cached data: {str(e)}")
    return None

def save_to_cache(df):
    """Save data to cache file"""
    try:
        cache_data = {
            'timestamp': time.time(),
            'data': df.to_dict(orient='records')
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except Exception as e:
        st.warning(f"Error saving to cache: {str(e)}")

def clean_numeric(value):
    """Clean and convert numeric values"""
    if isinstance(value, str):
        # Remove any non-numeric characters except decimal point and negative sign
        value = re.sub(r'[^\d.-]', '', value)
        try:
            return float(value)
        except ValueError:
            return 0
    return value

def determine_risk_level(returns, volatility):
    """Determine risk level based on returns and volatility"""
    if volatility < 5 and returns > 10:
        return 'Low'
    elif volatility < 10 and returns > 15:
        return 'Medium'
    else:
        return 'High'

def fetch_mutual_fund_data():
    """
    Fetch mutual fund data from Pakistan Mutual Funds Association
    """
    # Try to load cached data first
    cached_df = load_cached_data()
    if cached_df is not None:
        st.info("Using cached data. Data will be refreshed in the next update.")
        return cached_df

    try:
        # MUFAP website URL for NAV report
        url = "https://mufap.com.pk/Industry/IndustryStatDaily?tab=3"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        with st.spinner('Fetching latest mutual fund data from MUFAP...'):
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the main table containing fund data
            table = soup.find('table')
            if not table:
                st.error("Could not find fund data table on the website")
                return None
            
            # Extract fund data
            funds_data = []
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                try:
                    cols = row.find_all('td')
                    if len(cols) >= 14:  # Table has 14 columns
                        fund_data = {
                            'Sector': cols[0].text.strip(),
                            'AMC Name': cols[1].text.strip(),
                            'Fund Name': cols[2].text.strip(),
                            'Category': cols[3].text.strip(),
                            'Inception Date': cols[4].text.strip(),
                            'Offer': clean_numeric(cols[5].text.strip()),
                            'Repurchase': clean_numeric(cols[6].text.strip()),
                            'NAV': clean_numeric(cols[7].text.strip()),
                            'Validity Date': cols[8].text.strip(),
                            'Front-end Load': clean_numeric(cols[9].text.strip()),
                            'Back-end Load': clean_numeric(cols[10].text.strip()),
                            'Contingent Load': clean_numeric(cols[11].text.strip()),
                            'Management Fee': clean_numeric(cols[12].text.strip()),
                            'Trustee': cols[13].text.strip()
                        }
                        
                        # Calculate returns based on NAV
                        fund_data['Return_1Y'] = calculate_return(fund_data['NAV'])
                        
                        # Determine risk level based on category
                        risk_level = determine_risk_from_category(fund_data['Category'])
                        fund_data['Risk Level'] = risk_level
                        fund_data['Volatility'] = get_volatility_from_risk(risk_level)
                        
                        # Only include Open-End Funds
                        if fund_data['Sector'] == 'Open-End Funds':
                            funds_data.append(fund_data)
                except Exception as e:
                    st.warning(f"Error processing fund entry: {str(e)}")
                    continue
            
            if not funds_data:
                st.error("No valid fund data found")
                return None
            
            # Create DataFrame
            df = pd.DataFrame(funds_data)
            
            # Add timestamp
            df['Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Save to cache
            save_to_cache(df)
            
            return df
            
    except requests.RequestException as e:
        st.error(f"Error fetching data from MUFAP website: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def calculate_return(current_nav, historical=365):
    """
    Calculate returns (placeholder function)
    In a real implementation, this would use historical NAV data
    """
    # Placeholder calculation - replace with actual historical data comparison
    return (current_nav - 100) / 100 * 100

def determine_risk_from_category(category):
    """
    Determine risk level based on fund category
    """
    category = category.lower()
    if 'money market' in category or 'fixed rate' in category or 'capital protected' in category:
        return 'Low'
    elif 'income' in category or 'fund of funds' in category:
        return 'Medium'
    elif 'equity' in category or 'stock' in category or 'aggressive' in category:
        return 'High'
    else:
        return 'Medium'

def get_volatility_from_risk(risk_level):
    """
    Get estimated volatility based on risk level
    """
    risk_volatility = {
        'Low': 5.0,
        'Medium': 10.0,
        'High': 15.0
    }
    return risk_volatility.get(risk_level, 10.0)

def analyze_fund_performance(df):
    """
    Analyze mutual fund performance and generate insights
    """
    if df is None or df.empty:
        return None
    
    try:
        # Calculate basic statistics
        stats = {
            'Total Funds': len(df),
            'Average NAV': df['NAV'].mean(),
            'Best Performing Fund': df.loc[df['NAV'].idxmax(), 'Fund Name'],
            'Highest Risk Fund': df.loc[df['Risk Level'] == 'High', 'Fund Name'].iloc[0],
            'Average Front Load': df['Front-end Load'].mean(),
            'Average Management Fee': df['Management Fee'].mean()
        }
        
        return stats
    except Exception as e:
        st.error(f"Error calculating statistics: {str(e)}")
        return None

def generate_recommendations(df):
    """
    Generate investment recommendations based on fund performance
    """
    if df is None or df.empty:
        return []
    
    try:
        recommendations = []
        
        # Sort funds by performance
        top_performers = df.nlargest(5, 'Return_1Y')
        
        for _, fund in top_performers.iterrows():
            if fund['Return_1Y'] > 15 and fund['Risk Level'] == 'Low':
                recommendations.append({
                    'fund': fund['Fund Name'],
                    'message': f"Consider {fund['Fund Name']} for conservative investors",
                    'type': 'conservative'
                })
            elif fund['Return_1Y'] > 20 and fund['Risk Level'] == 'Medium':
                recommendations.append({
                    'fund': fund['Fund Name'],
                    'message': f"Consider {fund['Fund Name']} for moderate risk takers",
                    'type': 'moderate'
                })
            elif fund['Return_1Y'] > 25 and fund['Risk Level'] == 'High':
                recommendations.append({
                    'fund': fund['Fund Name'],
                    'message': f"Consider {fund['Fund Name']} for aggressive investors",
                    'type': 'aggressive'
                })
        
        return recommendations
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

def main():
    # Title and Navigation
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1>📈 Pakistan Mutual Funds Analyzer</h1>
            <p style='font-size: 1.2rem; color: #1e3a8a; margin-top: 1rem;'>
                Your Smart Investment Analysis Tool
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Top Navigation Bar
    st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        analysis_type = st.selectbox(
            "",  # Empty label
            ["Overview", "Performance Analysis", "Risk Assessment", "Recommendations"]
        )
    with col2:
        if st.button("🔄 Refresh Data"):
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
            st.experimental_rerun()
    with col3:
        st.markdown("""
            <div style='text-align: right; color: white; padding-top: 0.5rem;'>
                Powered by MUFAP
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Main content
    if analysis_type == "Overview":
        st.markdown("""
            <div class='custom-card'>
                <h2>Market Overview</h2>
                <p style='color: #6b7280; margin-bottom: 2rem;'>
                    Comprehensive analysis of Pakistan's mutual fund market
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        df = fetch_mutual_fund_data()
        if df is not None:
            stats = analyze_fund_performance(df)
            if stats:
                # Metrics in styled containers with better spacing
                st.markdown("""
                    <div style='margin: 2rem 0;'>
                        <h3>Key Metrics</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # First row of metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                        <div class='metric-card'>
                            <h4>Best Performing Fund</h4>
                            <p>{}</p>
                        </div>
                    """.format(stats['Best Performing Fund']), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class='metric-card'>
                            <h4>Highest Risk Fund</h4>
                            <p>{}</p>
                        </div>
                    """.format(stats['Highest Risk Fund']), unsafe_allow_html=True)
                
                # Second row of metrics
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown("""
                        <div class='metric-card'>
                            <h4>Total Funds</h4>
                            <p>{}</p>
                        </div>
                    """.format(stats['Total Funds']), unsafe_allow_html=True)
                
                with col4:
                    st.markdown("""
                        <div class='metric-card'>
                            <h4>Average NAV</h4>
                            <p>{:.2f}</p>
                        </div>
                    """.format(stats['Average NAV']), unsafe_allow_html=True)
                
                # Third row of metrics
                col5, col6 = st.columns(2)
                with col5:
                    st.markdown("""
                        <div class='metric-card'>
                            <h4>Average Front Load</h4>
                            <p>{:.2f}%</p>
                        </div>
                    """.format(stats['Average Front Load']), unsafe_allow_html=True)
                
                with col6:
                    st.markdown("""
                        <div class='metric-card'>
                            <h4>Average Management Fee</h4>
                            <p>{:.2f}%</p>
                        </div>
                    """.format(stats['Average Management Fee']), unsafe_allow_html=True)
                
                # Performance chart
                st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
                st.markdown("<h3>Performance Comparison</h3>", unsafe_allow_html=True)
                fig = px.bar(df, x='Fund Name', y='Return_1Y',
                           title="Fund Performance Comparison",
                           labels={'Return_1Y': 'One Year Return (%)', 'Fund Name': 'Fund'})
                fig.update_layout(
                    template="plotly_white",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Fund",
                    yaxis_title="One Year Return (%)",
                    showlegend=False,
                    hovermode='x unified',
                    font=dict(color='#1e3a8a'),
                    title_font=dict(size=20, color='#1e3a8a'),
                    xaxis=dict(showgrid=False, tickangle=45),
                    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                    bargap=0.2
                )
                fig.update_traces(
                    marker_color='#3b82f6',
                    hovertemplate='Return: %{y:.2f}%<extra></extra>'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Performance Analysis":
        st.header("Performance Analysis")
        df = fetch_mutual_fund_data()
        if df is not None:
            # Performance metrics
            st.subheader("Performance Metrics")
            performance_df = df[['Fund Name', 'Return_1Y']]
            st.dataframe(performance_df)
            
            # Performance trend
            fig = px.line(df, x='Fund Name', y='Return_1Y',
                         title="Performance Trend")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top performers
            st.subheader("Top Performing Funds")
            top_funds = df.nlargest(5, 'Return_1Y')
            fig = px.bar(top_funds, x='Fund Name', y='Return_1Y',
                        title="Top 5 Funds by 1-Year Return")
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Risk Assessment":
        st.header("Risk Assessment")
        df = fetch_mutual_fund_data()
        if df is not None:
            # Risk distribution
            fig = px.pie(df, names='Risk Level', title="Risk Level Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk vs Return scatter plot
            fig = px.scatter(df, x='Return_1Y', y='Risk Level',
                           size='NAV', color='Return_1Y',
                           title="Risk vs Return Analysis")
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk metrics table
            st.subheader("Risk Metrics")
            risk_df = df[['Fund Name', 'Risk Level', 'Volatility']]
            st.dataframe(risk_df)
    
    elif analysis_type == "Recommendations":
        st.header("Investment Recommendations")
        df = fetch_mutual_fund_data()
        if df is not None:
            recommendations = generate_recommendations(df)
            
            st.subheader("Recommended Funds")
            for rec in recommendations:
                if rec['type'] == 'conservative':
                    st.success(rec['message'])
                elif rec['type'] == 'moderate':
                    st.info(rec['message'])
                else:
                    st.warning(rec['message'])
            
            # Additional insights
            st.subheader("Market Insights")
            st.write("""
            - Consider diversifying your portfolio across different risk levels
            - Monitor fund performance regularly
            - Pay attention to expense ratios and management fees
            - Consider your investment horizon and risk tolerance
            - Keep track of market conditions and economic indicators
            - Review fund manager's track record and investment strategy
            """)

if __name__ == "__main__":
    main() 