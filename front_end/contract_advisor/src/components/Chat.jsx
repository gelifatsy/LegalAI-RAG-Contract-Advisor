import { useState } from 'react';

const Chat = () => {
  const [userInput, setUserInput] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });

      const data = await response.json();
      const newEntry = { query: userInput, answer: data.answer };
      setHistory([newEntry, ...history]);
    } catch (error) {
      console.error('Error fetching data:', error);
    }

    setLoading(false);
    setUserInput('');
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSubmit(event);
    }
  };

  return (
    <div className="chat-container flex flex-col items-center bg-lightblue w-full h-screen p-8 pt-12">
      <h1 className="chat-title text-5xl font-bold text-center text-gray-800 leading-tight mb-8">
        Lizzy AI<br />Your Contract Assistant
      </h1>
      <form className="chat-form flex flex-col items-center w-full">
        <textarea
          className="chat-input rounded-lg px-4 py-3 mb-4 border focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none w-2/5 text-center"
          placeholder="Enter your query..."
          value={userInput}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          style={{
            // Added shadow styles for 3D effect
            boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.22)',
            transform: 'translateY(4px)',
          }}
        />
        <button
          className="chat-submit-button bg-blue-500 text-white font-medium rounded-full px-12 py-3 shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          onClick={handleSubmit}
        >
          Send
        </button>
      </form>
      {loading && <div className="spinner" />} {/* Placeholder for spinner */}
      {history.map((entry, index) => (
        <div key={index} className="chat-output mt-4 border border-gray-300 rounded-lg p-4 bg-white" style={{ width: '50%', boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.22)', transform: 'translateY(4px)' }}>
          <p className="text-gray-700">User: {entry.query}</p>
          <p className="text-gray-700">Response: {entry.answer}</p>
        </div>
      ))}
    </div>
  );
};

export default Chat;
