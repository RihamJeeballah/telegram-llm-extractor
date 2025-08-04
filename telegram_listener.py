from telethon import TelegramClient, events
import pandas as pd
import os
from extractor import extract_fields
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from google.oauth2 import service_account
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def serialize_value(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value
# -------------------------
# ✅ Google Sheet Function
# -------------------------
def get_google_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Musa3nZ6-n_6xNODuQy2nxicSZl5WgC6s4ErK3dL20A/edit")
    return sheet.sheet1

# -------------------------
# ✅ Load environment
# -------------------------
load_dotenv()
api_id_str = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
if not api_id_str or not api_hash:
    raise ValueError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env")
api_id = int(api_id_str)

# -------------------------
# ✅ Settings
# -------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")
channels_to_listen = [-4909978596, -4890672685]  # Replace with your actual Telegram group/channel IDs
client = TelegramClient('session', api_id, api_hash)

# -------------------------
# ✅ Create Excel if missing
# -------------------------
def initialize_data_file():
    
    if not os.path.exists(DATA_FILE):
        columns = ["timestamp", "account_number", "name", "amount", "currency", "project", "details", "raw_message"]
        pd.DataFrame(columns=columns).to_excel(DATA_FILE, index=False)

# -------------------------
# ✅ Save to both Excel + Google Sheet
# -------------------------
def save_message(result):
    # Save to Excel
    try:
        df = pd.read_excel(DATA_FILE)
    except Exception as e:
        print(f"⚠️ Failed to load Excel: {e}")
        df = pd.DataFrame()

    df.loc[len(df)] = result
    df.to_excel(DATA_FILE, index=False)
    print("📁 Saved to local Excel")

    # Save to Google Sheet
    try:
        sheet = get_google_sheet()

        values = [
            serialize_value(result.get("timestamp")),
            result.get("account_number", ""),
            result.get("name", ""),
            result.get("amount", ""),
            result.get("currency", ""),
            result.get("project", ""),
            result.get("details", ""),
            result.get("raw_message", "")
        ]
        sheet.append_row(values)
        print("✅ Also saved to Google Sheet")
    except Exception as e:
        print(f"⚠️ Failed to write to Google Sheet: {e}")

# -------------------------
# ✅ Handle incoming messages
# -------------------------
@client.on(events.NewMessage(chats=channels_to_listen))
async def handler(event):
    text = event.raw_text
    print(f"📩 New message: {text}")

    result = extract_fields(text)
    result["timestamp"] = event.date.replace(tzinfo=None)
    result["raw_message"] = text

    save_message(result)

# -------------------------
# ✅ Run the listener
# -------------------------
def start_listener():
    initialize_data_file()
    client.start()
    print("👂 Telegram listener started...")
    client.run_until_disconnected()

if __name__ == "__main__":
    start_listener()
