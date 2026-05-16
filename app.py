import streamlit as st
import pandas as pd
import pdfplumber
import re

st.set_page_config(
    page_title="Banking Dashboard",
    layout="wide"
)

st.title(" Banking Dashboard")

st.sidebar.title("HDFC  Banking")

page = st.sidebar.selectbox(
    "Select Option",
    [
        "Dashboard",
        "Transactions"
    ]
)

st.subheader("Account Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Available Balance",
    "₹ 76,151"
)

col2.metric(
    "Total Credits",
    "₹ 2,45,000"
)

col3.metric(
    "Total Debits",
    "₹ 1,68,000"
)

uploaded_file = st.file_uploader(
    "Upload Bank Statement PDF",
    type=["pdf"]
)

def extract_transactions(pdf_file):

    transactions = []

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            for line in lines:

                pattern = r'(\d{2}/\d{2}/\d{2})'

                if re.search(pattern, line):

                    transactions.append({
                        "Transaction": line
                    })

    return pd.DataFrame(transactions)

if uploaded_file:

    st.success("PDF Uploaded Successfully")

    df = extract_transactions(uploaded_file)

    st.subheader("Transactions")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    st.metric(
        "Total Transactions",
        len(df)
    )

else:
    st.info("Upload your bank statement PDF")
