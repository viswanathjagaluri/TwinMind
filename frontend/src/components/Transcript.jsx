export default function Transcript({
    transcript,
    recording,
    startRecording,
    stopRecording
  }) {
    return (
      <div className="p-4 border-r flex flex-col">
        <h2 className="text-lg font-semibold mb-2">Transcript</h2>
  
        <div className="flex-1 overflow-y-auto bg-gray-800 p-2 rounded">
          {transcript || "Start speaking..."}
        </div>
  
        <button
          onClick={recording ? stopRecording : startRecording}
          className="mt-4 bg-blue-600 p-2 rounded"
        >
          {recording ? "Stop Mic" : "Start Mic"}
        </button>
      </div>
    );
  }