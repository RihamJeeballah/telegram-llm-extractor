from telethon import TelegramClient, events
import pandas as pd
import os
from extractor import extract_fields
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
data_file = 'data.xlsx'

# List of chat IDs to listen to (use negative values for channels/groups)
channels_to_listen = [-4909978596, -4890672685]

client = TelegramClient('session', api_id, api_hash)

# Initialize Excel file if it doesn't exist
if not os.path.exists(data_file):
    columns = ["timestamp", "account_number", "name", "amount", "currency", "project", "details", "raw_message"]
    pd.DataFrame(columns=columns).to_excel(data_file, index=False)

# Event listener for new messages
@client.on(events.NewMessage(chats=channels_to_listen))
async def handler(event):
    text = event.raw_text
    result = extract_fields(text)
    result["timestamp"] = event.date
    result["raw_message"] = text

    df = pd.read_excel(data_file)
    df.loc[len(df)] = result
    df.to_excel(data_file, index=False)
    print(f"✅ Message saved: {result}")

# Start the client
client.start()
client.run_until_disconnected()
