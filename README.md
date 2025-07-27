# Telegram LLM Extractor

This project listens to messages from private Telegram channels and uses OpenAI GPT-4 to extract structured data. Results are saved in Excel and displayed via a Streamlit dashboard.

## Features
- Real-time listening with Telethon
- LLM-based field extraction from Arabic messages
- Dashboard with filters and export

## Setup

1. Copy `.env.example` to `.env`
2. Fill in your credentials:
   - OpenAI API key
   - Telegram API ID + Hash

## Deploy to Railway

1. Push to GitHub
2. Connect the repo on [https://railway.app](https://railway.app)
3. Set the environment variables from `.env.example`
