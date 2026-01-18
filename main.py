import streamlit as st
import csv
import pandas as pd
from fpdf import FPDF
with open("data.csv",'r')as f:
    x=csv.reader(f)
    data=list(x)
    l=[data[i][1] for i in range(1,len(data))]
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
a=list(st.multiselect("Choose the tests from the below",options=l))
# Blood Test Prices
st.subheader("Select Blood Tests")
selected_test_costs=[]
for i in a:
    for j in data:
        if j[1]==i:
            selected_test_costs.append(int(j[2]))

# Calculate Bill
if a:
    cbill=[i for i in range(1,len(selected_test_costs)+1)]
    total_before_tax = sum(selected_test_costs)
    tax_amount = total_before_tax * (5 / 100)
    total_cost = total_before_tax + tax_amount
    b=st.button("Submit")
    if b:
        # Display Bill
        st.subheader("Bill Summary")
        bill_df = pd.DataFrame({
            "Test Name": a,
            "Cost (INR)": selected_test_costs
        })
        bill=bill_df.set_index([pd.Index([i for i in range(1,len(bill_df)+1)])])
        st.table(bill)
        st.write(f"*Total Before Tax:* INR {total_before_tax}")
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
        pdf.cell(200, 10, txt=f"Test Details:")
        pdf.ln(10)  # Add space
        
        # Table Header
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(20, 10, 'S.NO', 1)
        pdf.cell(100, 10, 'Test Name', 1)
        pdf.cell(40, 10, 'Cost (INR)', 1)
        pdf.ln()

        # Table Body
        pdf.set_font("Arial", size=12)
        for SNo ,test, cost in zip(cbill,a, selected_test_costs):
            pdf.cell(20, 10, f"{SNo}", 1)
            pdf.cell(100, 10, test, 1)
            pdf.cell(40, 10, f"{cost}", 1)
            pdf.ln()
        # Total, Tax, Final Cost
        

       

        pdf.cell(120, 10, 'Total before tax', 1)
        pdf.cell(40, 10, f"{total_before_tax}", 1)
        pdf.ln()

        pdf.cell(120, 10, f"Tax ({5}%)", 1)
        pdf.cell(40, 10, f"+{tax_amount}", 1)
        pdf.ln()

        pdf.cell(120, 10, 'Total Cost', 1)
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
