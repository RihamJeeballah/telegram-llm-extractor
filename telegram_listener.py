from telethon import TelegramClient, events
import pandas as pd
import os
from extractor import extract_fields
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
data_file = 'data.xlsx'

# List of private Telegram channel invite links
channels_to_listen = [
    "https://t.me/+j0428D5mADkxOTA0",
    "https://t.me/+SwIHHcR0C_wyNThk",
    "https://t.me/+zmLaoXZZ4PNhNjU0"
]

client = TelegramClient('session', api_id, api_hash)

if not os.path.exists(data_file):
    columns = ["timestamp", "account_number", "name", "amount", "currency", "project", "details", "raw_message"]
    pd.DataFrame(columns=columns).to_excel(data_file, index=False)

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

client.start()
client.run_until_disconnected()
