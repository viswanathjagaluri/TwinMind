from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

from services.groq_service import transcribe_audio, generate_chat_stream
from services.suggestion_engine import generate_suggestions
from services.transcript_service import SessionManager

app = FastAPI()

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    session_manager.create_session(session_id)

    try:
        while True:
            message = await websocket.receive()

            # 🎤 AUDIO
            if "bytes" in message:
                audio_bytes = message["bytes"]

                transcript_chunk = await transcribe_audio(audio_bytes)
                print("TRANSCRIPT:", transcript_chunk)

                if not transcript_chunk.strip():
                    continue

                session_manager.append_transcript(session_id, transcript_chunk)

                transcript = session_manager.get_transcript(session_id)
                recent_context = session_manager.get_recent_context(session_id)
                is_question = session_manager.is_recent_question(session_id)

                suggestions = await generate_suggestions(
                    transcript,
                    recent_context,
                    is_question
                )

                session_manager.add_suggestions(session_id, suggestions)

                await websocket.send_json({
                    "type": "update",
                    "transcript": transcript,
                    "suggestions": suggestions
                })

            # 💬 CHAT (STREAMING)
            elif "text" in message:
                data = json.loads(message["text"])

                if data["type"] == "chat":
                    transcript = session_manager.get_transcript(session_id)

                    # 🔥 STREAM RESPONSE TOKEN BY TOKEN
                    await generate_chat_stream(
                        websocket,
                        transcript,
                        data["message"]
                    )

    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")


# 📦 EXPORT
@app.get("/export/{session_id}")
def export_data(session_id: str):
    return session_manager.export(session_id)