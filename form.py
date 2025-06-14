import streamlit as st
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Page setup ---
logo = Image.open("logo.png")
st.set_page_config(page_title="TnBcS Inquiry", page_icon=logo, layout="centered")

# --- Google Sheets connection ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SERVICE_ACCOUNT_FILE = "tnbcs-credentials.json"

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open("TnBcS Prospects").sheet1

# --- Session State for Confirmation ---
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# --- If already submitted, show confirmation and redirect ---
if st.session_state.form_submitted:
    st.success("✅ Thank you! Our team will connect with you shortly.")
    st.markdown("You will be redirected to the [TnBcS Home Page](https://tnbcs.framer.website) shortly...")

    # Redirect after 5 seconds
    st.markdown("""
        <meta http-equiv="refresh" content="5;url=https://tnbcs.framer.website">
    """, unsafe_allow_html=True)

# --- Show Form ---
else:
    st.image("logo.png", width=120)
    st.title("Connect with TnBcS")
    st.write("We act as tunnels and bridges to overcome your business obstacles. Let’s build together!")
    st.markdown("Please fill out the form below. Our team will reach out to assist you.")

    with st.form("contact_form", clear_on_submit=False):
        name = st.text_input("Your Name *")
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number *")
        service = st.multiselect("Service Interested In", [
            "CRM", "Outsourcing Vendor Cycle", "Recruitment Tracker",
            "Approval Request System", "Performance Management", "Attendance Tracker",
            "Project Management", "Sales-Design-Tooling-Production", "Financial Module",
            "Inventory Management", "Shipping Management", "Machine Planning",
            "Downtime Tracking", "One-click MIS", "Hotel Booking System",
            "Quotation", "Invoicing", "Other"
        ])
        message = st.text_area("Additional Message")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Please fill all required fields marked with *.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                service_str = ", ".join(service)  # Convert list to string for Sheets
                sheet.append_row([timestamp, name, company, email, phone, ", ".join(service), message])
                st.session_state.form_submitted = True
                st.rerun()
   