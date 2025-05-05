# This is a simple Streamlit dashboard for exploring sales data from a CSV file.
# It allows users to filter the data by region and category, and displays the results in a table.
# Run from terminal: streamlit run my_dashboard.py

import streamlit as st
import pandas as pd

# --- Page Setup ---
# Set page config first - use wide mode makes tables look better
st.set_page_config(layout="wide")

# --- Data Loading ---
# Using cache so it doesn't reload the CSV every time we change a filter
@st.cache_data
def get_data(file_path):
    print(f"Attempting to load data from: {file_path}") # Good for debugging in terminal
    try:
        data = pd.read_csv(file_path, encoding='cp1252')
        # Attempt basic date conversion - might need later
        data['Order Date'] = pd.to_datetime(data['Order Date'], format='%m/%d/%Y', errors='coerce')
        print("Data loaded and date parsed.")
        return data
    except FileNotFoundError:
        st.error(f"Oops! Couldn't find the file: {file_path}")
        st.info("Make sure 'Superstore.csv' is in the same folder as the script.")
        return None # Return None if loading failed

# Load the superstore data
store_data = get_data('Superstore.csv')

# --- App Interface ---
st.title("📊 Superstore Explorer App")
st.write("Use the filters in the sidebar to explore the sales data.")

# Only proceed if data was loaded successfully
if store_data is not None:

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filters")

    # Make a dropdown for Region
    # Get unique regions, sort them, and add 'All' at the start
    region_options = ['All'] + sorted(store_data['Region'].unique())
    chosen_region = st.sidebar.selectbox("Pick a Region:", region_options)

    # Make a dropdown for Category
    category_options = ['All'] + sorted(store_data['Category'].unique())
    chosen_category = st.sidebar.selectbox("Pick a Category:", category_options)

    # --- Filtering Logic ---
    # Start with the full dataset, then apply filters one by one
    filtered_data = store_data.copy() # Important to copy!

    if chosen_region != 'All':
        print(f"Filtering by Region: {chosen_region}") # Debug print
        filtered_data = filtered_data[filtered_data['Region'] == chosen_region]

    if chosen_category != 'All':
        print(f"Filtering by Category: {chosen_category}") # Debug print
        filtered_data = filtered_data[filtered_data['Category'] == chosen_category]

    # --- Display Results ---
    st.header("Filtered Results")
    st.markdown(f"Showing data for **{chosen_region}** region and **{chosen_category}** category.")
    st.write(f"Found **{len(filtered_data)}** matching records.")

    # Show the actual data table
    # st.dataframe is interactive, st.table is static
    st.dataframe(filtered_data)

    # Show some quick summary numbers below the table
    if not filtered_data.empty:
        st.subheader("Quick Summary (for filtered data):")

        # Calculate totals / averages
        sum_sales = filtered_data['Sales'].sum()
        sum_profit = filtered_data['Profit'].sum()
        avg_discount_perc = filtered_data['Discount'].mean() * 100 # As percentage

        # Use columns for a cleaner layout
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${sum_sales:,.2f}")
        col2.metric("Total Profit", f"${sum_profit:,.2f}")
        col3.metric("Avg. Discount", f"{avg_discount_perc:.1f}%") # One decimal place

else:
    # Show a message if data loading failed earlier
    st.warning("Data loading failed, cannot display the dashboard content.")