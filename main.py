import streamlit as st
import pandas as pd
from fpdf import FPDF

# Title
st.set_page_config(page_title='clinic',page_icon="icon.webp")
col1,col2=st.columns(2)
col1.image("cliniclogo.jpg",width=250)
col2.title("Welcome to Blood Test Bill Generator")
# Patient Information Form
with st.form("Patient Information"):
    st.subheader("Patient Information")
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
    patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    test_date = st.date_input("Date of Test[yyyy/mm/dd]")
    submit_info = st.form_submit_button("Submit")

# Blood Test Prices
test_prices = {
    "Complete Blood Count (CBC)": 500,
    "Lipid Profile": 800,
    "Liver Function Test (LFT)": 700,
    "Kidney Function Test (KFT)": 650,
    "Thyroid Profile": 600,
    "Blood Sugar (Fasting)": 300,
    "Hemoglobin A1C": 450,
}

# Select Blood Tests
st.subheader("Select Blood Tests")
selected_tests = st.multiselect("Blood Tests", options=list(test_prices.keys()))
# Calculate Bill
if selected_tests:
    selected_test_costs = [test_prices[test] for test in selected_tests]
    total_before_tax = sum(selected_test_costs)
    tax_amount = total_before_tax * (5/ 100)
    total_cost = total_before_tax + tax_amount

    # Display Bill
    st.subheader("Bill Summary")
    bill_df = pd.DataFrame({
        "Test Name": selected_tests,
        "Cost (INR)": selected_test_costs
    })
    st.table(bill_df)
    st.write(f"*Total Before Discount:* INR {total_before_tax}")
    st.write(f"*Tax Amount ({5}%):* INR {tax_amount}")
    st.write(f"### *Total Cost:* INR {total_cost}")


    # Save as PDF with Table
    if st.button("Save as PDF"):
        pdf = FPDF()
        pdf.add_page()

        # Add title and patient information
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt=f"Blood Test Bill for {patient_name}", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {patient_age} | Gender: {patient_gender}", ln=True)
        pdf.cell(200, 10, txt=f"Date of Test: {test_date}", ln=True)
        pdf.cell(200, 10, txt="Test Details:")
        pdf.ln(10)  # Add space
    
        # Table Header
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(100, 10, 'Test Name', 1)
        pdf.cell(40, 10, 'Cost (INR)', 1)
        pdf.ln()

        # Table Body
        pdf.set_font("Arial", size=12)
        for test, cost in zip(selected_tests, selected_test_costs):
            pdf.cell(100, 10, test, 1)
            pdf.cell(40, 10, f"{cost}", 1)
            pdf.ln()

        # Total, Tax, Final Cost
        pdf.cell(100, 10, f"Tax ({5}%)", 1)
        pdf.cell(40, 10, f"+{tax_amount}", 1)
        pdf.ln()

        pdf.cell(100, 10, 'Total Cost', 1)
        pdf.cell(40, 10, f"{total_cost}", 1)
        pdf.ln()

        # Save PDF
        pdf_output = f"{patient_name}_blood_test_bill.pdf"
        pdf.output(pdf_output)

        # Download the PDF
        with open(pdf_output, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button(
            label="Download Bill as PDF",
            data=pdf_data,
            file_name=pdf_output,
            mime="application/pdf"
        )
else:
    st.warning("Please select at least one test.")
