import pandas as pd
import streamlit as st
import altair as alt
from datetime import date  # Import 'date' from the 'datetime' module

try:
    # Load data
    url = "https://github.com/JayatiPatel/streamlit_dashboard/raw/main/Coffee_Chain_Sales.csv"
    df = pd.read_csv(url)

    df['Date'] = pd.to_datetime(df['Date'], format='%y-%m-%d')  # Correctly convert the 'Date' column

    # Check if the required columns exist
    required_columns = ['Product_line', 'AreaCode', 'Date', 'Sales', 'Profit', 'Marketing', 'Total_expenses']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Column '{col}' not found in the dataset.")
            st.stop()

    # Streamlit app
    st.title("Sales and Marketing Dashboard")

    # Sidebar for slicers with multi-select options
    selected_product_line = st.sidebar.multiselect("Select Product Lines", df['Product_line'].unique())
    selected_area_code = st.sidebar.multiselect("Select Area Codes", df['AreaCode'].unique())
    selected_product_type = st.sidebar.multiselect("Select Product Types", df['Product_type'].unique())
    selected_state = st.sidebar.multiselect("Select States", df['State'].unique())

    # Check if filters are applied
    filters_applied = selected_product_line or selected_area_code or selected_product_type or selected_state

    # Filter data based on slicers or display full data
    filtered_df = df if not filters_applied else df[
        (df['Product_line'].isin(selected_product_line)) &
        (df['AreaCode'].isin(selected_area_code)) &
        (df['Product_type'].isin(selected_product_type)) &
        (df['State'].isin(selected_state))
    ]

    # Set green color schemes
    green_color_scheme = alt.Scale(range=['#238b45', '#66c2a4', '#ccece6', '#a1d99b', '#005824'])

    # Query 1: Sales Performance Over Time
    st.subheader("Query 1: Sales Performance Over Time")
    chart1 = alt.Chart(filtered_df).mark_line().encode(
        x='Date:T',
        y='Sales:Q',
        color=alt.value('#238b45'),  # Explicitly set the color to the first shade of green
    ).properties(width=600, height=300)
    st.altair_chart(chart1)

    # Query 2: Product-wise Profitability
    st.subheader("Query 2: Product-wise Profitability")
    chart2 = alt.Chart(filtered_df).mark_circle().encode(
        x='Sales:Q',
        y='Profit:Q',
        color=alt.Color('Product:N', scale=green_color_scheme),
    ).properties(width=600, height=300)
    st.altair_chart(chart2)

    # Query 3: Marketing Expense vs. Sales
    st.subheader("Query 3: Marketing Expense vs. Sales")
    chart4 = alt.Chart(filtered_df).mark_circle().encode(
        x='Marketing:Q',
        y='Sales:Q',
        color=alt.value('#238b45'),  # Explicitly set the color to the first shade of green
    ).properties(width=600, height=300)
    st.altair_chart(chart4)

    # Query 4: Contribution to Total Sales (Pie Chart)
    st.subheader("Query 4: Contribution to Total Sales")
    pie_data = filtered_df.groupby('Product_line')['Sales'].sum().reset_index()
    chart5 = alt.Chart(pie_data).mark_arc().encode(
        theta='Sales:Q',
        color=alt.Color('Product_line:N', scale=green_color_scheme),
    ).properties(width=600, height=300)
    st.altair_chart(chart5)

    # Query 5: Type of Expense Breakdown (Bar Chart)
    st.subheader("Query 5: Type of Expense Breakdown")
    bar_data2 = filtered_df.groupby('Type')['Total_expenses'].sum().reset_index()
    chart6 = alt.Chart(bar_data2).mark_bar().encode(
        x='Type:N',
        y='Total_expenses:Q',
        color=alt.Color('Type:N', scale=green_color_scheme),
    ).properties(width=600, height=300)
    st.altair_chart(chart6)

    # Query 6: Product-wise Target vs. Actual Sales
    if 'Target_sales' in df.columns:
        st.subheader("Query 6: Product-wise Target vs. Actual Sales")
        bar_data = filtered_df[['Product', 'Target_sales', 'Sales']].melt('Product')
        chart7 = alt.Chart(bar_data).mark_bar().encode(
            x='Product:N',
            y='value:Q',
            color=alt.Color('variable:N', scale=green_color_scheme),
        ).properties(width=600, height=300)
        st.altair_chart(chart7)
    else:
        st.warning("Column 'Target_sales' not found in the dataset.")

except pd.errors.EmptyDataError:
    st.error("Error: Empty dataset.")
except Exception as e:
    st.error(f"Error: {e}")
