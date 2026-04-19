import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"


# 🎤 Whisper Transcription
async def transcribe_audio(audio_bytes):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{BASE_URL}/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}"
                },
                files={
                    "file": ("audio.webm", audio_bytes, "audio/webm")
                },
                data={
                    "model": "whisper-large-v3"
                }
            )

        res_json = response.json()
        print("WHISPER RESPONSE:", res_json)

        if "text" not in res_json:
            return ""

        return res_json.get("text", "")

    except Exception as e:
        print("Whisper Exception:", str(e))
        return ""


# 💬 NORMAL CHAT (fallback)
async def generate_chat_response(transcript, question):
    prompt = f"""
You are a real-time AI assistant.

Answer clearly and concisely.

Rules:
- Keep answer SHORT (3–6 lines max)
- Use bullet points if helpful
- Avoid long paragraphs

Transcript:
{transcript[-3000:]}

Question:
{question}
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
                    "temperature": 0.3
                }
            )

        res_json = response.json()

        if "choices" not in res_json:
            return "Couldn't generate response."

        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        print("Chat Exception:", str(e))
        return "Something went wrong."


# 🔥 STREAMING CHAT (REAL-TIME TOKENS)
async def generate_chat_stream(websocket, transcript, question):
    prompt = f"""
You are a real-time AI assistant.

Answer clearly and concisely.

Rules:
- Keep answers short
- Use simple readable sentences
- Prefer bullet points

Transcript:
{transcript[-3000:]}

Question:
{question}
"""

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True
                }
            ) as response:

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    if line.startswith("data: "):
                        data = line.replace("data: ", "")

                        if data == "[DONE]":
                            break

                        try:
                            json_data = json.loads(data)
                            delta = json_data["choices"][0]["delta"]

                            if "content" in delta:
                                await websocket.send_json({
                                    "type": "stream",
                                    "token": delta["content"]
                                })

                        except Exception:
                            continue

        # ✅ signal end of stream
        await websocket.send_json({
            "type": "stream_end"
        })

    except Exception as e:
        print("Streaming Exception:", str(e))

        # fallback message
        await websocket.send_json({
            "type": "stream",
            "token": "Something went wrong while streaming response."
        })

        await websocket.send_json({
            "type": "stream_end"
        })