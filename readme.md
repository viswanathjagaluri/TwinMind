# 🧠 TwinMind AI Copilot

A **real-time AI-powered meeting assistant** that listens to conversations, transcribes speech, generates intelligent suggestions, and provides interactive AI chat — inspired by tools like TwinMind and modern AI copilots.

---

## 🚀 Overview

TwinMind AI Copilot is a full-stack application that enables **live conversation intelligence**. It captures audio from the user’s microphone, converts it into text using Whisper, analyzes the context using LLMs, and provides:

* Real-time transcript
* Smart suggestions
* AI-powered chat responses
* Streaming (token-by-token) output like ChatGPT

---

## ✨ Key Features

### 🎤 Live Audio Transcription

* Real-time microphone input
* Speech-to-text using **Groq Whisper API**
* Continuous transcript updates

---

### 💡 Context-Aware Suggestions

* Generates intelligent suggestions based on conversation
* Detects:

  * Questions
  * Discussions
* Produces:

  * Follow-up questions
  * Insights
  * Fact-checks

---

### 💬 AI Chat Assistant

* Ask questions based on conversation
* Click suggestions to auto-send
* Chat interface includes:

  * Typing animation
  * Streaming responses (real-time tokens)
  * Clean UI (ChatGPT-style)

---

### ⚡ Real-Time Streaming

* AI responses stream token-by-token
* No waiting for full response
* Smooth conversational UX

---

### 🎧 Listening Animation

* Visual waveform animation when mic is active
* Pulsing indicator for recording state

---

### 📦 Export Session

* Download full session data:

  * Transcript
  * Suggestions
  * Chat history
* Export as JSON

---

## 🏗️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* WebSocket (real-time communication)

### Backend

* FastAPI
* WebSockets (async streaming)
* Groq API:

  * Whisper (speech-to-text)
  * LLM (chat + suggestions)
* Python (httpx, async)

---

## 📁 Project Structure

```
twinmind-app/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ListeningAnimation.jsx
│   │   │   ├── Transcript.jsx
│   │   │   ├── Suggestions.jsx
│   │   │   ├── Chat.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │
│   └── tailwind.config.js
│
├── backend/
│   ├── main.py
│   ├── services/
│   │   ├── groq_service.py
│   │   ├── suggestion_engine.py
│   │   ├── transcript_service.py
│   ├── requirements.txt
│   ├── .env
│
└── README.md
```

---

# ⚙️ SETUP INSTRUCTIONS

---

## 🔧 Backend Setup

### 1. Navigate to backend

```bash
cd backend
```

---

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If needed:

```bash
pip install fastapi uvicorn httpx python-dotenv websockets
```

---

### 4. Create `.env` file

Inside `backend/`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 5. Run backend server

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## 🎨 Frontend Setup

### 1. Navigate to frontend

```bash
cd frontend
```

---

### 2. Install dependencies

```bash
npm install
```

---

### 3. Run frontend

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🔌 How the System Works

---

### 🎤 Step 1: Audio Capture

* User clicks **Start Mic**
* Audio is recorded using MediaRecorder API

---

### 🔄 Step 2: WebSocket Streaming

* Audio chunks sent to backend via WebSocket

---

### 🧠 Step 3: Transcription

* Backend sends audio to Whisper API
* Converts speech → text

---

### 💡 Step 4: Suggestions Engine

* Uses recent context
* Detects:

  * Question vs discussion
* Generates smart suggestions

---

### 💬 Step 5: Chat Interaction

* User clicks suggestion or types message
* Sent to backend

---

### ⚡ Step 6: Streaming Response

* AI response streamed token-by-token
* Frontend renders live typing effect

---

# 🎯 Example Workflow

User says:

```
"We are discussing AI latency issues"
```

System generates:

* What latency target are we aiming for?
* Consider caching strategies
* Check model size impact

User clicks → AI responds instantly

---

# 🧠 Architecture Highlights

* Event-driven WebSocket architecture
* Async backend processing
* Context-aware AI prompting
* Streaming LLM responses
* Real-time UI updates

---

# 📸 UI Features

* ChatGPT-style chat bubbles
* Typing animation
* Loading indicators
* Auto-scroll transcript
* Interactive suggestion cards

---

# 🚀 Future Enhancements

* User authentication (JWT)
* Multi-user sessions
* Persistent storage (PostgreSQL / Redis)
* Deployment (Vercel + Render)
* Advanced NLP intent detection
* Real-time collaborative sessions

---

# 🎥 Demo (Optional)

*Add demo video or screenshots here*

---

# 👨‍💻 Author

**Madhav Vaddepalli**

---

# ⭐ Why This Project Matters

This project demonstrates:

* Real-time system design
* AI/LLM integration
* WebSocket streaming architecture
* Full-stack engineering
* Production-level UI/UX thinking

---

# 📜 License

MIT License
