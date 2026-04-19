export default function Suggestions({ suggestions, onClickSuggestion }) {
    return (
      <div className="p-4 border-r">
        <h2 className="text-lg font-semibold mb-2">Suggestions</h2>
  
        {suggestions?.map((s, i) => (
          <div
            key={i}
            onClick={() => onClickSuggestion(s.text)}
            className="bg-gray-800 p-3 my-2 rounded cursor-pointer hover:bg-gray-700"
          >
            <p className="text-sm text-gray-400">{s.type}</p>
            <p>{s.text}</p>
          </div>
        ))}
      </div>
    );
  }