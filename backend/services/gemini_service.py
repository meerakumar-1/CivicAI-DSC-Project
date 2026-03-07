import os
import json
import asyncio
from google import genai
from google.genai.errors import ServerError
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


async def analyze_issue(description: str, fallback_department: str):

    prompt = f"""
    A citizen reported the following civic issue:

    {description}

    Determine:
    1. Correct department
    2. Priority (low, medium, high)

    Return ONLY valid JSON in this format:

    {{
        "department": "...",
        "priority": "..."
    }}
    """

    retries = 3

    for attempt in range(retries):

        try:

            loop = asyncio.get_event_loop()

            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
            )

            text = response.text

            data = json.loads(text)

            return {
                "department": data.get("department", fallback_department),
                "priority": data.get("priority", "medium")
            }

        except ServerError:
            # retry on 503
            await asyncio.sleep(2)

        except Exception:
            break

    # FAILSAFE fallback
    return {
        "department": fallback_department,
        "priority": "medium"
    }