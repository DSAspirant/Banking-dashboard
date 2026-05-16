import streamlit as st

st.title("Banking Dashboard")

uploaded_file = st.file_uploader(
    "Upload Bank Statement PDF",
    type=["pdf"]
)

if uploaded_file:
    st.success("PDF Uploaded Successfully")
else:
    st.info("Upload your bank statement PDF")
