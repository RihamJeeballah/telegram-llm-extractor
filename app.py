# ✅ Updated app.py (Streamlit Dashboard with Google Sheets)
import streamlit as st
import pandas as pd
import gspread
import os
import json
from google.oauth2.service_account import Credentials

# --------------------------
# ✅ Function to load live data
# --------------------------
def load_data_from_google_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1Musa3nZ6-n_6xNODuQy2nxicSZl5WgC6s4ErK3dL20A/edit"
    )
    worksheet = sheet.sheet1

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# --------------------------
# ✅ Streamlit UI
# --------------------------
st.set_page_config(page_title="Telegram Information Extractor", layout="wide")
st.title("📊 Telegram Extraction Dashboard")
st.markdown("Monitor and explore structured messages extracted from your Telegram channel in real time.")

# --------------------------
# ✅ Load data
# --------------------------
try:
    df = load_data_from_google_sheet()
except Exception as e:
    st.error(f"❌ Failed to load data from Google Sheets: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ No data found yet. Please wait for messages to be received.")
    st.stop()

# --------------------------
# ✅ Summary metrics
# --------------------------
st.subheader("📌 Summary")
col1, col2 = st.columns(2)
col1.metric("📄 Total Entries", len(df))
col2.metric("🧑‍💼 Unique Names", df['name'].nunique())

# --------------------------
# ✅ Search / Filter
# --------------------------
st.subheader("🔍 Search & Filter")
with st.expander("Click to filter table"):
    search_name = st.text_input("Search by Name")
    search_account = st.text_input("Search by Account Number")
    search_project = st.text_input("Search by Project")

    filtered_df = df.copy()
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].astype(str).str.contains(search_name, case=False, na=False)]
    if search_account:
        filtered_df = filtered_df[filtered_df['account_number'].astype(str).str.contains(search_account)]
    if search_project:
        filtered_df = filtered_df[filtered_df['project'].astype(str).str.contains(search_project, case=False, na=False)]

# --------------------------
# ✅ Show table + download
# --------------------------
st.subheader("🧾 Extracted Messages")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download as CSV", data=csv, file_name="telegram_extracted_data.csv", mime="text/csv")

# --------------------------
# ✅ Show full table (raw)
# --------------------------
with st.expander("🗂 View Raw Google Sheet Data"):
    st.dataframe(df, use_container_width=True)
