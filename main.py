import streamlit as st
import pandas as pd

# Load the Excel file and read the specific sheets
excel_file_path = 'PortalView.xlsx'  # replace with your actual Excel file path
sheets = pd.read_excel(excel_file_path, sheet_name=["Year1", "Year2", "Year3", "Year4"])  # First 4 sheets

# Strip any extra spaces in column names to avoid issues
for sheet_name in sheets:
    sheets[sheet_name].columns = sheets[sheet_name].columns.str.strip()

# Combine roll number data from all sheets into a single DataFrame
all_data = pd.concat([sheets[sheet].copy() for sheet in sheets], ignore_index=True)

# Select unique roll numbers for the dropdown
roll_numbers = all_data['RollNo'].unique()

# Streamlit app title
st.title("Fee Portal")

# Dropdown for selecting Roll Number
selected_roll = st.selectbox("Select Roll Number", roll_numbers)

# Filter data based on selected Roll Number
student_data = all_data[all_data['RollNo'] == selected_roll]

if not student_data.empty:
    # Display student details in a structured format
    st.subheader("Student Details")
    st.write("**Roll No:**", student_data.iloc[0]['RollNo'])
    st.write("**Student Name:**", student_data.iloc[0]['Name'])

    # Display fee details for each year
    st.subheader("Fee Details")
    total_fees = 0
    for year, sheet_data in sheets.items():
        year_data = sheet_data[sheet_data['RollNo'] == selected_roll]
        if not year_data.empty:
            if 'TOTAL DUE' in year_data.columns:
                total_due = year_data.iloc[0]['TOTAL DUE'] if pd.notna(year_data.iloc[0]['TOTAL DUE']) else "Not Found"
                st.write(f"{year}: {total_due}")
                if pd.notna(year_data.iloc[0]['TOTAL DUE']):
                    total_fees += year_data.iloc[0]['TOTAL DUE']
            else:
                st.write(f"{year}: 'TOTAL DUE' column not found")
        else:
            st.write(f"{year}: Not Found")

    # Display the total fees
    st.write("**Total Fees:**", total_fees)
else:
    st.error("No data found for the selected Roll Number.")
