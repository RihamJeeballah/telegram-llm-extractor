import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_fields(message_text):
    prompt = f"""
You are an information extractor.

Your task is to extract structured fields from the Arabic message provided below and return only a valid JSON object. Do not include any text, explanation, or formatting — only the JSON.

Return JSON in this exact format:
{{
  "account_number": "string",
  "name": "string",
  "amount": "string",
  "currency": "string",
  "project": "string",
  "details": "string"
}}

Message:
"""{message_text}"""
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print("❌ JSON extraction failed:", e)
        return {
            "account_number": "",
            "name": "",
            "amount": "",
            "currency": "",
            "project": "",
            "details": ""
        }
