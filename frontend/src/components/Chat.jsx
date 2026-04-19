import { useState } from "react";

export default function Chat({ chat, sendChat }) {
    const [input, setInput] = useState("");

    const handleSend = () => {
        sendChat(input);
        setInput("");
    };

    return (
        <div className="p-4 flex flex-col">
            <h2 className="text-lg font-semibold mb-2">Chat</h2>

            <div className="flex-1 overflow-y-auto bg-gray-800 p-2 rounded">
                {chat.map((c, i) => (
                    <div key={i} className="mb-3">
                        <p className="text-blue-400">{c.question}</p>
                        <p>{c.answer}</p>
                    </div>
                ))}
            </div>

            <div className="mt-2 flex">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-1 p-2 bg-gray-700 rounded"
                />
                <button
                    onClick={handleSend}
                    className="ml-2 bg-green-600 px-4 rounded"
                >
                    Send
                </button>
            </div>
        </div>
    );
}