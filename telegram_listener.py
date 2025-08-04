from telethon import TelegramClient, events
import pandas as pd
import os
from extractor import extract_fields
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")

channels_to_listen = [-4909978596, -4890672685]

client = TelegramClient('session', api_id, api_hash)

# Initialize Excel file if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        columns = [
            "timestamp", "account_number", "name", "amount", "currency",
            "project", "details", "machinery", "raw_message"
        ]
        pd.DataFrame(columns=columns).to_excel(DATA_FILE, index=False)

# Handler to append new message
@client.on(events.NewMessage(chats=channels_to_listen))
async def handler(event):
    text = event.raw_text
    print(f"📩 Received: {text}")

    result = extract_fields(text)
    result["timestamp"] = event.date.replace(tzinfo=None)
    result["raw_message"] = text

    try:
        df = pd.read_excel(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)

    print(f"✅ Message saved: {result}")

# Main listener
def start_listener():
    initialize_data_file()
    client.start()
    print("👂 Listening to Telegram messages...")
    client.run_until_disconnected()

# Run directly
if __name__ == "__main__":
    import asyncio

    # Create and set new event loop for Railway
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_listener()
