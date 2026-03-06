import os
import json
from dotenv import load_dotenv
<<<<<<< HEAD
from google import genai
=======
import asyncio
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

async def analyze_issue(description: str):

    prompt = f"""
You are an AI that classifies civic complaints.

A citizen reported the following issue:

Description: {description}

Determine:
1. The most appropriate department
2. Priority level (low, medium, high)
3. Priority Score, whole number between 0 and 100

Possible departments:
Road
Electricity
Water
Sanitation
BBMP

Return ONLY valid JSON in this format:

{{
  "department": "...",
  "priority": "...",
  "priority_score": "..."
}}
"""

<<<<<<< HEAD
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
=======
    loop = asyncio.get_event_loop()
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)

    response = await loop.run_in_executor(
        None,
        lambda: model.generate_content(prompt)
    )
    try:
        data = json.loads(response.text)
        return data
    except:
        return {
            "department": "BBMP",
            "priority": "medium"
        }