# extractor.py
import os
import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

def extract_fields(message_text):
    json_template = {
        "account_number": "",
        "name": "",
        "amount": "",
        "currency": "",
        "machinery": "",
        "project": "",
        "details": ""
    }

    prompt = (
        "You are an information extractor.\n\n"
        "Your task is to extract structured fields from the following Arabic message and return only a valid JSON object.\n"
        "Do not include any explanation, markdown, or text — only return JSON matching the template below exactly.\n\n"
        f"Message:\n{message_text}\n\n"
        f"Here is the JSON template to be filled in:\n{json.dumps(json_template, ensure_ascii=False)}"
    )

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # moved inside
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```json") or content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except Exception as e:
        print("❌ JSON extraction failed:", e)
        return json_template
