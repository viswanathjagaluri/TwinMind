import { useEffect, useRef, useState } from "react";
import ListeningAnimation from "./components/ListeningAnimation";

export default function App() {
  const [transcript, setTranscript] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [chat, setChat] = useState([]);
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);

  const [loading, setLoading] = useState(false);
  const [typingText, setTypingText] = useState("");

  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const transcriptRef = useRef(null);

  const sessionId = "session1";

  // 🔌 WebSocket
  useEffect(() => {
    const WS_URL =
      import.meta.env.VITE_WS_URL || "ws://localhost:8000";

    const ws = new WebSocket(`${WS_URL}/ws/${sessionId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "update") {
        setTranscript(data.transcript);
        setSuggestions(data.suggestions);
      }

      if (data.type === "chat") {
        setLoading(false);
        simulateTyping(data.answer, data.question);
      }
    };

    wsRef.current = ws;

    return () => ws.close();
  }, []);

  // 🎤 Mic
  const toggleRecording = async () => {
    if (recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const recorder = new MediaRecorder(stream, {
      mimeType: "audio/webm",
    });

    mediaRecorderRef.current = recorder;

    recorder.ondataavailable = async (event) => {
      if (event.data.size > 0) {
        const arrayBuffer = await event.data.arrayBuffer();
        wsRef.current.send(arrayBuffer);
      }
    };

    recorder.start(7000);
    setRecording(true);
  };

  // 💬 Send message
  const sendMessage = (msg) => {
    if (!msg) return;

    setLoading(true);

    wsRef.current.send(
      JSON.stringify({
        type: "chat",
        message: msg,
      })
    );

    setInput("");
  };

  // ⌨️ Typing animation
  const simulateTyping = (fullText, question) => {
    let index = 0;
    setTypingText("");

    const interval = setInterval(() => {
      setTypingText((prev) => prev + fullText[index]);
      index++;

      if (index >= fullText.length) {
        clearInterval(interval);

        setChat((prev) => [
          ...prev,
          { question, answer: fullText },
        ]);

        setTypingText("");
      }
    }, 10);
  };

  // 📜 Auto-scroll transcript
  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop =
        transcriptRef.current.scrollHeight;
    }
  }, [transcript]);

  // 📦 Export
  const exportSession = async () => {
    const res = await fetch(
      `http://localhost:8000/export/${sessionId}`
    );
    const data = await res.json();

    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "session.json";
    a.click();
  };

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-white">

      {/* HEADER */}
      <div className="px-6 py-4 border-b border-gray-800 flex justify-between items-center">
        <h1 className="text-xl font-semibold">TwinMind AI Copilot</h1>

        <button
          onClick={exportSession}
          className="bg-green-600 px-3 py-1 rounded text-xs"
        >
          Export
        </button>
      </div>

      {/* MAIN GRID */}
      <div className="grid grid-cols-3 flex-1">

        {/* 🎤 TRANSCRIPT */}
        <div className="border-r border-gray-800 p-5 flex flex-col">

          <div className="flex justify-between items-center mb-3">
            <h2 className="text-xs text-gray-400">LIVE TRANSCRIPT</h2>

            <div className="flex items-center gap-2">
              <button
                onClick={toggleRecording}
                className={`px-3 py-1.5 rounded text-xs flex items-center gap-2 ${recording
                  ? "bg-red-600 shadow-lg shadow-red-500/50"
                  : "bg-blue-600"
                  }`}
              >
                {recording && (
                  <span className="w-2 h-2 bg-white rounded-full animate-ping"></span>
                )}
                {recording ? "Stop Listening..." : "Start"}
              </button>

              {recording && <ListeningAnimation />}
            </div>
          </div>

          <div
            ref={transcriptRef}
            className="flex-1 overflow-y-auto bg-gray-900 rounded-lg p-4 text-sm"
          >
            {transcript || "Start speaking..."}
          </div>
        </div>

        {/* 💡 SUGGESTIONS */}
        <div className="border-r border-gray-800 p-5 flex flex-col">
          <h2 className="text-xs text-gray-400 mb-3">
            LIVE SUGGESTIONS
          </h2>

          <div className="flex-1 overflow-y-auto space-y-3">
            {suggestions.map((s, i) => (
              <div
                key={i}
                onClick={() => sendMessage(s.text)}
                className="bg-gray-900 p-4 rounded-lg cursor-pointer hover:border-blue-500 border border-gray-800 transition transform hover:scale-[1.02]"
              >
                <p className="text-xs text-blue-400 uppercase">
                  {s.type}
                </p>
                <p className="text-sm mt-1">{s.text}</p>
              </div>
            ))}
          </div>
        </div>

        {/* 💬 CHAT */}
        <div className="p-5 flex flex-col">
          <h2 className="text-xs text-gray-400 mb-3">CHAT</h2>

          <div className="flex-1 overflow-y-auto space-y-4">

            {chat.map((c, i) => (
              <div key={i} className="space-y-2">

                {/* USER */}
                <div className="bg-blue-600 px-3 py-2 rounded-lg text-sm w-fit ml-auto">
                  {c.question}
                </div>

                {/* AI */}
                <div className="bg-gray-800 px-3 py-2 rounded-lg text-sm whitespace-pre-line">
                  {c.answer.split("\n").map((line, idx) => (
                    <p key={idx}>
                      {line.startsWith("-") || line.startsWith("*")
                        ? "• " + line.slice(1)
                        : line}
                    </p>
                  ))}
                </div>
              </div>
            ))}

            {/* ✨ Typing */}
            {typingText && (
              <div className="bg-gray-800 px-3 py-2 rounded-lg text-sm whitespace-pre-line">
                {typingText}
                <span className="animate-pulse">|</span>
              </div>
            )}

            {/* ⏳ Loading */}
            {loading && (
              <div className="text-gray-400 text-sm animate-pulse">
                AI is thinking...
              </div>
            )}
          </div>

          <div className="mt-4 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 px-3 py-2 bg-gray-800 rounded-md outline-none text-sm"
            />

            <button
              onClick={() => sendMessage(input)}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-md text-sm"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}