# Pakistan Mutual Funds Analyzer

A Streamlit application that analyzes mutual funds data from Pakistan Mutual Funds Association and provides investment recommendations.

## Features

- Real-time data fetching from PMFA
- Performance analysis and visualization
- Risk assessment
- Investment recommendations
- Interactive charts and metrics

## Setup

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, use the following command:

```bash
streamlit run app.py
```

The application will open in your default web browser.

## Usage

1. Use the sidebar to navigate between different analysis views:

   - Overview: General market statistics and performance metrics
   - Performance Analysis: Detailed fund performance comparison
   - Risk Assessment: Risk level distribution and analysis
   - Recommendations: Investment suggestions based on fund performance

2. Interact with the charts and tables to explore the data
3. View investment recommendations based on fund performance and risk levels

## Note

The current version uses placeholder data. To use real data, you'll need to implement the actual data fetching logic in the `fetch_mutual_fund_data()` function in `app.py`.
