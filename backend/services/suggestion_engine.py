import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"


async def generate_suggestions(transcript: str, recent_context: str, is_question: bool):
    # 🧠 limit context
    context = recent_context[-1000:] if recent_context else ""
    full = transcript[-2000:] if transcript else ""

    # 🎯 dynamic behavior
    if is_question:
        behavior = """
The last user input is a QUESTION.

You MUST:
- Provide 1 direct ANSWER
- Provide 1 follow-up QUESTION
- Provide 1 INSIGHT
"""
    else:
        behavior = """
The conversation is a DISCUSSION.

You MUST:
- Provide 1 follow-up QUESTION
- Provide 1 INSIGHT
- Provide 1 FACT-CHECK or clarification
"""

    prompt = f"""
You are a real-time AI meeting copilot.

{behavior}

Rules:
- EXACTLY 3 suggestions
- Each must be 1 sentence only
- Must be highly relevant to the MOST RECENT context
- Be concise, actionable, and helpful
- Avoid repetition

Recent Context:
{context if context.strip() else "No recent context"}

Full Transcript:
{full if full.strip() else "No conversation yet"}

Return ONLY valid JSON:
[
  {{"type": "answer", "text": "..."}},
  {{"type": "question", "text": "..."}},
  {{"type": "insight", "text": "..."}}
]
"""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.4
                }
            )

        res_json = response.json()
        print("GROQ RAW RESPONSE:", res_json)

        # 🚨 API safety
        if "choices" not in res_json:
            return fallback_suggestions("API error")

        content = res_json["choices"][0]["message"]["content"]
        print("MODEL OUTPUT:", content)

        # ✅ try JSON parse
        try:
            parsed = json.loads(content)

            if isinstance(parsed, list):
                return parsed[:3]

        except Exception:
            pass

        # 🔄 fallback parse
        return parse_text_fallback(content)

    except Exception as e:
        print("ERROR in suggestion engine:", str(e))
        return fallback_suggestions(str(e))


#  fallback parser
def parse_text_fallback(content: str):
    lines = content.split("\n")
    suggestions = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # remove numbering
        line = line.lstrip("1234567890.- ")

        suggestions.append({
            "type": "suggestion",
            "text": line
        })

    if suggestions:
        return suggestions[:3]

    return fallback_suggestions("Parsing failed")


#  fallback suggestions
def fallback_suggestions(reason="unknown"):
    print("Using fallback suggestions due to:", reason)

    return [
        {
            "type": "question",
            "text": "Can you clarify the main topic being discussed?"
        },
        {
            "type": "insight",
            "text": "It may help to summarize the key points so far."
        },
        {
            "type": "fact-check",
            "text": "Ensure the information shared is accurate and up to date."
        }
    ]