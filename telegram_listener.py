from telethon import TelegramClient, events
import pandas as pd
import os
from extractor import extract_fields
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Telegram credentials
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Absolute path to the Excel file
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")

# Chat IDs of the Telegram groups/channels to monitor
channels_to_listen = [-4909978596, -4890672685]

# Initialize the Telegram client session
client = TelegramClient('session', api_id, api_hash)

# Initialize the Excel file if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        columns = ["timestamp", "account_number", "name", "amount", "currency",
                   "project", "details", "raw_message"]
        pd.DataFrame(columns=columns).to_excel(DATA_FILE, index=False)

# Message handler to extract data and save it
@client.on(events.NewMessage(chats=channels_to_listen))
async def handler(event):
    text = event.raw_text
    print(f"📩 Received: {text}")
    
    result = extract_fields(text)
    result["timestamp"] = event.date.replace(tzinfo=None)
    result["raw_message"] = text

    # Load the Excel file and append the new row
    df = pd.read_excel(DATA_FILE)
    df.loc[len(df)] = result
    df.to_excel(DATA_FILE, index=False)
    
    print(f"✅ Message saved: {result}")

# Main function to run the listener
def start_listener():
    initialize_data_file()
    client.start()
    print("👂 Listening to Telegram messages...")
    client.run_until_disconnected()

# Only run if executed directly (not when imported)
if __name__ == "__main__":
    start_listener()
