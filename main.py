import streamlit as st
import pandas as pd

# Load the Excel file and all sheets
excel_path = "PortalView.xlsx"  # Update this path if needed
sheets = pd.read_excel(excel_path, sheet_name=["Year1", "Year2", "Year3", "Year4"])

# Combine all data into a single DataFrame
all_data = pd.concat(sheets.values(), keys=sheets.keys()).reset_index(level=0).rename(columns={"level_0": "Year"})

# Extract unique roll numbers
roll_numbers = all_data['RollNo'].unique()

# Light/Dark Mode Toggle
st.set_page_config(page_title="Fee Portal", layout="wide")
dark_mode = st.toggle("🌙 Dark Mode")

# Apply custom styling
if dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #1e1e1e; color: white; }
        .stSelectbox, .stTextInput, .stButton { background-color: #333333 !important; color: white !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: #f0f2f6; color: black; }
        .stSelectbox, .stTextInput, .stButton { background-color: white !important; color: black !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

# App Title
st.markdown("<h1 style='text-align: center;'>🎓 Fee Portal</h1>", unsafe_allow_html=True)

# Dropdown for Roll Number Selection
selected_roll_no = st.selectbox("Select Roll Number", roll_numbers)

# Display Student Details
if selected_roll_no:
    student_data = all_data[all_data['RollNo'] == selected_roll_no]
    if not student_data.empty:
        student_name = student_data['Name'].iloc[0] if 'Name' in student_data.columns else "Name Not Found"
        
        st.markdown("""---""")
        st.subheader("📌 Student Details")
        st.write(f"**🎓 Roll No:** {selected_roll_no}")
        st.write(f"**👤 Student Name:** {student_name}")
        
        # Fee Details
        st.markdown("""---""")
        st.subheader("💰 Fee Details")
        total_due = 0
        for year, year_data in student_data.groupby("Year"):
            yearly_due = year_data['TOTAL DUE'].sum()
            total_due += yearly_due
            st.write(f"**📅 {year}:** {yearly_due if yearly_due > 0 else '0'}")
        st.write(f"**📊 Total Fee Due:** {total_due}")
    else:
        st.warning("No data available for the selected roll number.")

# Overall Summary Section
st.markdown("""---""")
st.subheader("📈 Overall Summary")

# Define Prefix Groups
group1_prefixes = ("21B", "22B")
group2_prefixes = ("216", "226")

# Remove NaN Roll Numbers
filtered_data = all_data.dropna(subset=['RollNo'])

# Compute Total Dues
group1_total = filtered_data[filtered_data['RollNo'].str.startswith(group1_prefixes)]['TOTAL DUE'].sum()
group2_total = filtered_data[filtered_data['RollNo'].str.startswith(group2_prefixes)]['TOTAL DUE'].sum()
overall_total_due = all_data['TOTAL DUE'].sum()

st.write(f"**🏫 Total Dues for {group1_prefixes}:** {group1_total}")
st.write(f"**🏫 Total Dues for {group2_prefixes}:** {group2_total}")
st.write(f"**📊 Overall Total Dues:** {overall_total_due}")

# Footer
st.markdown("""<hr style='border: 1px solid gray;'>""", unsafe_allow_html=True)
st.write("Developed by **Prasad Chowdary**")
