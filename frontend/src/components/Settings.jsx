import { useState } from "react";

export default function Settings() {
    const [key, setKey] = useState("");

    const saveKey = () => {
        localStorage.setItem("groq_key", key);
        alert("Saved!");
    };

    return (
        <div className="fixed bottom-4 right-4 bg-gray-800 p-4 rounded shadow">
            <input
                placeholder="Groq API Key"
                value={key}
                onChange={(e) => setKey(e.target.value)}
                className="p-2 bg-gray-700 rounded"
            />
            <button onClick={saveKey} className="ml-2 bg-blue-600 px-3 rounded">
                Save
            </button>
        </div>
    );
}