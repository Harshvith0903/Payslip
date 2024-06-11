import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Define a function to create the payslip PDF
class PDF(FPDF):
    def header(self):
        self.image('LOGO.png', 10, 8, 33)  # Insert the logo on the top left corner
        self.set_font("Arial", 'B', 12)
        self.cell(0, 5, "SYMBIOSYS TECHNOLOGIES", ln=True, align='C')
        self.cell(0, 5, "Plot No 1&2, Hill no-2, IT Park,", ln=True, align='C')
        self.cell(0, 5, "Rushikonda, Visakhapatnam-45", ln=True, align='C')
        self.cell(0, 5, "Ph: 2550369, 2595657", ln=True, align='C')
        self.ln(20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_payslip(employee):
    pdf = PDF()
    pdf.add_page()
    
    # Add the payslip title
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "SALARY STATEMENT FOR THE MONTH OF JANUARY 2024", ln=True, align='C')
    pdf.ln(5)
    
    # Table 1: Employee Code, Name, Designation
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(65, 8, "Employee Code", border=1)
    pdf.cell(65, 8, "Employee Name", border=1)
    pdf.cell(65, 8, "Designation", border=1)
    pdf.ln()
    pdf.set_font("Arial", size=10)
    pdf.cell(65, 8, f"{employee['Employee Code']}", border=1)
    pdf.cell(65, 8, f"{employee['Employee Name']}", border=1)
    pdf.cell(65, 8, f"{employee['Designation']}", border=1)
    pdf.ln(10)
    
    # Table 2: Date of Joining, Employment Status, Statement for the month
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(65, 8, "Date of Joining", border=1)
    pdf.cell(65, 8, "Employment Status", border=1)
    pdf.cell(65, 8, "Statement for the month", border=1)
    pdf.ln()
    pdf.set_font("Arial", size=10)
    date_of_joining = pd.to_datetime(employee['Date of Joining']).strftime('%d-%m-%Y')
    pdf.cell(65, 8, f"{date_of_joining}", border=1)
    pdf.cell(65, 8, f"{employee['Employment Status']}", border=1)
    pdf.cell(65, 8, "", border=1)
    pdf.ln(10)
    
    # Table 3 and 4: Classified Income and Deductions side by side
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 8, "Classified Income", border=1, align='C')
    pdf.cell(30, 8, "Amount (Rs.)", border=1, align='C')
    pdf.cell(60, 8, "Deductions", border=1, align='C')
    pdf.cell(30, 8, "Amount (Rs.)", border=1, align='C')
    pdf.ln()
    pdf.set_font("Arial", size=10)
    
    income_items = [
        "Basic Pay (Rs.)", "House Rent Allowance (Rs.)", 
        "City Compensatory Allowance (Rs.)", "Travel Allowance (Rs.)", 
        "Food Allowance (Rs.)", "Performance Incentives (Rs.)"
    ]
    deduction_items = [
        "Professional Tax (Rs.)", "Income Tax (Rs.)", 
        "Provident Fund (Rs.)", "ESI (Rs.)", 
        "Leaves-Loss of Pay (Rs.)", "Others (Rs.)"
    ]
    
    for income, deduction in zip(income_items, deduction_items):
        pdf.cell(70, 8, f"{income.replace('(Rs.)', '').strip()}", border=1)
        pdf.cell(30, 8, f"Rs. {employee[income]:.2f}", border=1, align='R')
        pdf.cell(60, 8, f"{deduction.replace('(Rs.)', '').strip()}", border=1)
        pdf.cell(30, 8, f"Rs. {employee[deduction]:.2f}", border=1, align='R')
        pdf.ln()
    
    # Add spacing before the Totals section
    pdf.ln(10)
    
    # Totals section
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 8, "GROSS PAY", border=1)
    pdf.cell(30, 8, f"Rs. {employee['Gross Pay (Rs.)']:.2f}", border=1, align='R')
    pdf.cell(60, 8, "DEDUCTIONS", border=1)
    pdf.cell(30, 8, f"Rs. {employee['Deductions (Rs.)']:.2f}", border=1, align='R')
    pdf.ln()
    pdf.cell(100, 8, "NET PAY", border=1)
    pdf.cell(80, 8, f"Rs. {employee['Net Pay (Rs.)']:.2f}", border=1, align='R')
    pdf.ln(20)
    
    # Footer section with added spacing
    pdf.cell(0, 8, "AUTHORISED SIGNATORY", ln=True)
    pdf.ln(20)  # Added more spacing here
    pdf.cell(0, 8, "Durgaaprasadh,", ln=True)
    pdf.cell(0, 8, "H.R Executive", ln=True)
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 8, "We request you to verify employment details with our office on email: hr@symbiosystech.com. (+91-0891-2550369)", ln=True)

    return pdf

# Streamlit app
st.title("Employee Payslip Generator")

# Step 1: Upload the Excel file
uploaded_file = st.file_uploader("Upload Employee Data (Excel file)", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Data Loaded Successfully")

    # Display the DataFrame
    st.dataframe(df)

    # Step 2: Select Employee ID
    employee_id = st.selectbox("Select Employee ID", df["Employee Code"].unique())

    if st.button("Generate Payslip"):
        # Filter the DataFrame for the selected employee
        employee = df[df["Employee Code"] == employee_id].squeeze()

        if not employee.empty:
            payslip_pdf = create_payslip(employee)
            output_path = f"{employee['Employee Code']}.pdf"
            payslip_pdf.output(output_path)

            # Display download link for the PDF
            with open(output_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="Download Payslip PDF",
                    data=pdf_bytes,
                    file_name=output_path,
                    mime="application/octet-stream"
                )

            # Clean up
            os.remove(output_path)
        else:
            st.error("Employee ID not found.")
