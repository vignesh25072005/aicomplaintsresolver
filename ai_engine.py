
import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def analyze_complaint(complaint: str) -> dict:
    """Analyze a customer complaint and generate a resolution."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI customer support assistant.

Analyze the complaint below and return ONLY a valid JSON object.
Do not use Markdown fences.

Complaint:
{complaint}

Return these fields:
{{
  "category": "A short complaint category",
  "sentiment": "Positive, Neutral, or Negative",
  "priority": "Low, Medium, or High",
  "summary": "A one-sentence summary of the problem",
  "resolution": "A practical recommended resolution",
  "reply": "A professional, empathetic reply to the customer"
}}

Rules:
- Base your answer on the complaint.
- Do not claim a refund, replacement, or action has already happened.
- Recommend verification when order, payment, or account details are needed.
- Never request passwords, PINs, or OTPs.
- Do not invent company policies or promise a specific outcome.
- Use High priority only when the complaint indicates urgency or
  significant impact; otherwise choose a reasonable priority.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        },
    )

    if not response.text:
        raise ValueError("The AI model returned an empty response.")

    result = json.loads(response.text)

    required_fields = [
        "category",
        "sentiment",
        "priority",
        "summary",
        "resolution",
        "reply",
    ]

    for field in required_fields:
        if field not in result or not isinstance(result[field], str):
            raise ValueError(f"The AI response is missing a valid {field}.")

    result["priority"] = result["priority"].capitalize()
    result["sentiment"] = result["sentiment"].capitalize()

    if result["priority"] not in {"Low", "Medium", "High"}:
        result["priority"] = "Medium"

    if result["sentiment"] not in {"Positive", "Neutral", "Negative"}:
        result["sentiment"] = "Neutral"

    return result
