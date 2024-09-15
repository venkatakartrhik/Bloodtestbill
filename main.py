import streamlit as st
import pandas as pd
from fpdf import FPDF

# Title
st.set_page_config(page_title='clinic',page_icon="icon.webp")
col1,col2,col3=st.columns(3)
col1.image("cliniclogo.jpg",width=200)
col2.header("Welcome to Blood Test Bill Generator")
# Patient Information Form

st.subheader("Patient Information")
patient_name = st.text_input("Patient Name")
patient_age = st.text_input("Patient Age")
patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
test_date = st.date_input("Date of Test[yyyy/mm/dd]")
# Blood Test Prices
test_prices = {
    "CBP":300,"ESR":50,"BLOOD SUGAR":30,
    "BLOOD UREA":75,"SERUMCREATININE":75,"SERUM BILIRUBIN":100,
    "LFT":800,"LIPD PROFILE":350,"MP(KIT)":200,
    "DENGUE":800,"WIDAL":100,"BLOOD GROUP":50,
    "HIV(TRIDOT)":250,"HBsAG":100,"HCV":250,
    "VDRL":70,"BT CT":50,"URIC ACID":150,
    "CALCIUM":150,"RA FACTOR":300,"CRP":300,
    "ASO":400,"THYROID":450,"URINE ROUTINE":100,
    "ELECTROLYTES":500,"HBA1c":500,"TOTAL PROTIENS":200,
    "HAEMOGLOBIN":50,"ECG":100,"IRON TEST":400,
}
# Select Blood Tests
st.subheader("Select Blood Tests")
selected_tests = st.multiselect("Blood Tests", options=list(test_prices.keys()))
# Additional Charges/Discounts
discount = st.slider("Discount (%)", 0, 50, 0)
# Calculate Bill
if selected_tests:
    selected_test_costs = [test_prices[test] for test in selected_tests]
    total_before_discount = sum(selected_test_costs)
    discount_amount = total_before_discount * (discount / 100)
    subtotal = total_before_discount - discount_amount
    tax_amount = subtotal * (5 / 100)
    total_cost = subtotal + tax_amount
    b=st.button("Submit")
    if b:
        # Display Bill
        st.subheader("Bill Summary")
        bill_df = pd.DataFrame({
            "Test Name": selected_tests,
            "Cost (INR)": selected_test_costs
        })
        st.table(bill_df)
        st.write(f"*Total Before Discount:* INR {total_before_discount}")
        st.write(f"*Discount Amount ({discount}%):* INR {discount_amount}")
        st.write(f"*Subtotal After Discount:* INR {subtotal}")
        st.write(f"*Tax Amount ({5}%):* INR {tax_amount}")
        st.write(f"### *Total Cost:* INR {total_cost}")



        pdf = FPDF()
        pdf.add_page()
        # Add title and patient information
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt=f"Blood Test Bill for {patient_name}", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {patient_age} | Gender: {patient_gender}", ln=True)
        pdf.cell(200, 10, txt=f"Date of Test: {test_date}", ln=True)
        pdf.cell(300, 10, txt="Test Details:")
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
        pdf.cell(100, 10, 'Total Before Discount', 1)
        pdf.cell(40, 10, f"{total_before_discount}", 1)
        pdf.ln()

        pdf.cell(100, 10, f"Discount ({discount}%)", 1)
        pdf.cell(40, 10, f"-{discount_amount}", 1)
        pdf.ln()

        pdf.cell(100, 10, 'Subtotal After Discount', 1)
        pdf.cell(40, 10, f"{subtotal}", 1)
        pdf.ln()

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
