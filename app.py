import streamlit as st
import pandas as pd
import pdfplumber
import re

st.set_page_config(
    page_title="Banking Dashboard",
    layout="wide"
)

st.title("🏦 Banking Dashboard")

st.sidebar.title("🏦 HDFC Banking")

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

                    parts = line.split(" ")

                    date = parts[0]

                    transactions.append({
                        "Date": date,
                        "Transaction": line
                    })

    return pd.DataFrame(transactions)

if uploaded_file:

    st.success("PDF Uploaded Successfully")

    df = extract_transactions(uploaded_file)

    if "Date" in df.columns:

        selected_date = st.selectbox(
            "Filter By Date",
            ["All"] + list(df["Date"].unique())
        )

        if selected_date != "All":

            df = df[
                df["Date"] == selected_date
            ]

    st.subheader("Transactions")

    search = st.text_input(
        "Search Transactions"
    )

    if search:

        df = df[
            df["Transaction"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    limit = st.selectbox(
        "Transactions Per Page",
        [10, 25, 50, "All"]
    )

    if limit != "All":

        df = df.head(limit)

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
