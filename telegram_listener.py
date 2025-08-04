from telethon import TelegramClient, events
import pandas as pd
import os
from extractor import extract_fields
from dotenv import load_dotenv

# Load environment variables from .env (for local dev)
load_dotenv()

# --------- Set up Telegram credentials safely --------- #
api_id_str = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

if not api_id_str or not api_hash:
    raise ValueError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in environment variables")

api_id = int(api_id_str)

# --------- Define data storage path --------- #
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")

# --------- Define which channels to listen to --------- #
channels_to_listen = [-4909978596, -4890672685]  # Replace with your actual group/channel IDs

# --------- Initialize Telegram client --------- #
client = TelegramClient('session', api_id, api_hash)

# --------- Initialize the Excel file if it doesn't exist --------- #
def initialize_data_file():
    print("📁 Saving to:", DATA_FILE)  # ✅ Add this line
    if not os.path.exists(DATA_FILE):
        columns = ["timestamp", "account_number", "name", "amount", "currency",
                   "project", "details", "raw_message"]
        pd.DataFrame(columns=columns).to_excel(DATA_FILE, index=False)

# --------- Handle new incoming messages --------- #
@client.on(events.NewMessage(chats=channels_to_listen))
async def handler(event):
    text = event.raw_text
    print(f"📩 Received: {text}")

    result = extract_fields(text)
    result["timestamp"] = event.date.replace(tzinfo=None)
    result["raw_message"] = text

    try:
        df = pd.read_excel(DATA_FILE)
    except Exception as e:
        print(f"⚠️ Failed to load Excel file: {e}")
        df = pd.DataFrame()

    df.loc[len(df)] = result
    df.to_excel(DATA_FILE, index=False)

    print(f"✅ Message saved: {result}")

# --------- Entry point for listener --------- #
def start_listener():
    initialize_data_file()
    client.start()
    print("👂 Listening to Telegram messages...")
    print("📁 Saving to:", DATA_FILE)  # Optional: shows during actual runtime
    client.run_until_disconnected()

# Run only when script is executed directly (not imported)
if __name__ == "__main__":
    start_listener()
