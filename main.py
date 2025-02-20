import streamlit as st
import pandas as pd

# Load the Excel file and all sheets
excel_path = "PortalView.xlsx"  # Update this path if needed
sheets = pd.read_excel(excel_path, sheet_name=["Year1", "Year2", "Year3", "Year4"])

# Combine all data into a single DataFrame for easier manipulation
all_data = pd.concat(sheets.values(), keys=sheets.keys()).reset_index(level=0).rename(columns={"level_0": "Year"})

# Extract unique roll numbers
roll_numbers = all_data['RollNo'].unique()

# Set page configuration for dark/light mode
dark_mode = st.toggle("Dark Mode")

if dark_mode:
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stSelectbox, .stTextInput {
            background-color: #333;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .stSelectbox, .stTextInput {
            background-color: #f0f0f0;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Title for the app
st.title("Fee Portal")

# Dropdown to select a roll number
selected_roll_no = st.selectbox("Select Roll Number", roll_numbers)

# Display the selected student's details
if selected_roll_no:
    student_data = all_data[all_data['RollNo'] == selected_roll_no]

    if not student_data.empty:
        student_name = student_data['Name'].iloc[0] if 'Name' in student_data.columns else "Name Not Found"

        st.subheader("Student Details")
        st.write(f"**Roll No:** {selected_roll_no}")
        st.write(f"**Student Name:** {student_name}")

        # Calculate and display total dues for each year and the grand total for the selected student
        st.subheader("Fee Details")
        total_due = 0
        for year, year_data in student_data.groupby("Year"):
            yearly_due = year_data['TOTAL DUE'].sum()
            total_due += yearly_due
            st.write(f"**{year}:** {yearly_due if yearly_due > 0 else '0'}")
        st.write(f"**Total Fee Due:** {total_due}")
    else:
        st.write("0 for the selected roll number.")

# Calculate and display cumulative totals by prefix groups
st.subheader("Overall Summary")

# Define the prefix groups
group1_prefixes = ("21B", "22B")
group2_prefixes = ("216", "226")

# Filter out rows where 'RollNo' is NaN before using str.startswith
filtered_data = all_data.dropna(subset=['RollNo'])

# Calculate total dues by prefix group
group1_total = filtered_data[filtered_data['RollNo'].str.startswith(group1_prefixes)]['TOTAL DUE'].sum()
group2_total = filtered_data[filtered_data['RollNo'].str.startswith(group2_prefixes)]['TOTAL DUE'].sum()

st.write(f"**Total Dues for Roll Numbers starting with {group1_prefixes}:** {group1_total}")
st.write(f"**Total Dues for Roll Numbers starting with {group2_prefixes}:** {group2_total}")

# Display overall total due for all students
overall_total_due = all_data['TOTAL DUE'].sum()
st.write(f"**Overall Total Dues for All Students:** {overall_total_due}")
