import streamlit as st
import pandas as pd
import os
import threading


st.set_page_config(page_title="Telegram Information Extractor", layout="wide")
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")

st.title("📊 Telegram Extraction Dashboard")
st.markdown("Monitor and explore structured messages extracted from your Telegram channel in real time.")

if os.path.exists(DATA_FILE):
    df = pd.read_excel(DATA_FILE)
else:
    st.warning("⚠️ No data found yet. Please wait for the Telegram listener to receive messages.")
    st.stop()

st.subheader("📌 Summary")
col1, col2 = st.columns(2)
col1.metric("📄 Total Entries", len(df))
col2.metric("🧑‍💼 Unique Names", df['name'].nunique())

st.subheader("🔍 Search & Filter")
with st.expander("Click to filter table"):
    search_name = st.text_input("Search by Name")
    search_account = st.text_input("Search by Account Number")
    search_project = st.text_input("Search by Project")

    filtered_df = df.copy()
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]
    if search_account:
        filtered_df = filtered_df[filtered_df['account_number'].astype(str).str.contains(search_account)]
    if search_project:
        filtered_df = filtered_df[filtered_df['project'].str.contains(search_project, case=False, na=False)]

st.subheader("🧾 Extracted Messages")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download as CSV", data=csv, file_name="telegram_extracted_data.csv", mime="text/csv")

with st.expander("🗂 View Raw Database (Full Excel File)"):
    st.dataframe(df, use_container_width=True)
