from datetime import datetime


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "transcript": "",
                "chunks": [],          #  recent transcript chunks
                "suggestions": [],
                "chat": []
            }

    #  Append transcript + store chunks
    def append_transcript(self, session_id, text):
        session = self.sessions[session_id]

        session["transcript"] += " " + text
        session["chunks"].append(text)

        # Keep only last N chunks (context window)
        if len(session["chunks"]) > 10:
            session["chunks"].pop(0)

    # Full transcript
    def get_transcript(self, session_id):
        return self.sessions[session_id]["transcript"]

    #  Context-aware recent transcript
    def get_recent_context(self, session_id):
        return " ".join(self.sessions[session_id]["chunks"])

    # Detect if last chunk is a question
    def is_recent_question(self, session_id):
        chunks = self.sessions[session_id]["chunks"]

        if not chunks:
            return False

        last = chunks[-1].lower()

        return (
            "?" in last
            or last.startswith(("what", "why", "how", "when", "where", "can", "is", "are", "do"))
        )

    # 💡 Store suggestions
    def add_suggestions(self, session_id, suggestions):
        self.sessions[session_id]["suggestions"].append({
            "time": datetime.utcnow().isoformat(),
            "data": suggestions
        })

    # 💬 Chat storage
    def add_chat(self, session_id, question, answer):
        self.sessions[session_id]["chat"].append({
            "time": datetime.utcnow().isoformat(),
            "question": question,
            "answer": answer
        })

    # 📦 Export session
    def export(self, session_id):
        return self.sessions.get(session_id, {})