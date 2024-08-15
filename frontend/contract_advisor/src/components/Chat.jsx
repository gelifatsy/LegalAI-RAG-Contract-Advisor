import React, { useState, useEffect, useCallback } from 'react';
import ChatSidebar from './chatSidebar';

const Chat = () => {
  const [userInput, setUserInput] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]); 
  const [uploadingFiles, setUploadingFiles] = useState({});

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

  const handleFileChange = (event) => {
    console.log('Event object:', event);
    if (event) {
      setSelectedFile(event);
    } else {
      console.error('Invalid event object passed to handleFileChange');
    }
  };


  
  const handleFileUpload = useCallback(() => {
    if (selectedFile) {
      setUploadingFiles((prevFiles) => ({ ...prevFiles, [selectedFile.name]: true }));
      const formData = new FormData();
      formData.append('file', selectedFile);
  
      fetch('http://localhost:8000/upload', { 
        method: 'POST',
        body: formData,
      })
        .then(response => {
          return response.text();
        })
        .then(data => {
          console.log('File uploaded successfully!');
          setUploadedFiles((prevFiles) => [...prevFiles, selectedFile.name]);
          setUploadingFiles((prevFiles) => ({ ...prevFiles, [selectedFile.name]: false }));
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          setUploadingFiles((prevFiles) => ({ ...prevFiles, [selectedFile.name]: false }));
        });
    }
  }, [selectedFile, setUploadedFiles]);
  

  useEffect(() => {
    console.log('Uploaded files:', uploadedFiles);
  }, [uploadedFiles]);

  return (
    <div className="chat-container flex flex-col items-center bg-lightblue w-full h-screen">
  
      <div className="chat-content flex flex-row items-start w-full" style={{ height: 'calc(100vh - 200px)' }}>
        <div className="chat-sidebar w-1/4" style={{ backgroundColor: '#e0f2f7' }}> 
          <ChatSidebar handleFileChange={handleFileChange} handleFileUpload={handleFileUpload} uploadedFiles={uploadedFiles} />
        </div>
  
        <div className="chat-main flex flex-col items-start w-3/4 ml-4" style={{ borderLeft: '1px solid #ddd', boxShadow: '2px 0px 4px rgba(0, 0, 0, 0.1)' }}> 
        <h1 className="chat-title text-5xl font-bold text-center text-gray-800 leading-tight mb-8 px-80 py-2">
  Lizzy AI<br />Your Contract Assistant
</h1>
          <div className="chat-history flex flex-col items-start w-full overflow-y-auto" style={{ height: 'calc(100vh - 380px)' }}> 
            {history.map((entry, index) => (
              <div key={index} className="chat-output mt-4 border border-gray-300 rounded-lg p-4 bg-white" style={{ width: '50%', boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.22)', transform: 'translateY(4px)' }}>
                <p className="text-gray-700">User: {entry.query}</p>
                <p className="text-gray-700">Response: {entry.answer}</p>
              </div>
            ))}
          </div>
          <div className="chat-form flex items-center w-full p-4">
            <textarea
              className="chat-input rounded-lg px-4 py-3 mb-4 border focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none w-full text-center" 
              placeholder="Enter your query..."
              value={userInput}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              style={{
                boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.22)',
                transform: 'translateY(4px)',
              }}
            />
            <button
              className="chat-submit-button bg-blue-500 text-white font-medium rounded-lg px-8 py-3 ml-4 shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              onClick={handleSubmit}
            >
              Send
            </button>
          </div>
          {loading && <div className="spinner" />} 
        </div>
      </div>

    </div>
  );
};
  
export default Chat;