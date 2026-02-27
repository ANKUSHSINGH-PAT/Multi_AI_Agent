from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b" 

def explain(activities, errors, warnings):

    prompt = f"""
You are an expert UiPath RPA architect.

Activities:
{activities}

Errors:
{errors}

Warnings:
{warnings}

Explain clearly:
1. What problems exist
2. Why they are risky
3. How to fix them in UiPath
4. Optimization suggestions

Respond in bullet points.
"""

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a senior RPA architect."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content