import React, { useState, useEffect } from 'react';
import { MdChat } from 'react-icons/md';

const ChatSidebar = ({ handleFileChange, handleFileUpload, uploadedFiles }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [localUploadedFiles, setLocalUploadedFiles] = useState([]);

  useEffect(() => {
    setLocalUploadedFiles(uploadedFiles);
  }, [uploadedFiles]);

  const handleFileChangeProp = (event) => {
    const selectedFile = event.target.files[0];
    handleFileChange(selectedFile);
    handleFileUpload();
  };
  

  return (
    <div className="chat-sidebar w-full bg-white p-4 rounded-lg" style={{ boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)' }}>
      <div className="mb-12"> {/* Increased spacing */}
        <span className="text-lg font-semibold flex items-center">
          New Chat
          <MdChat size={24} onClick={() => console.log('Icon clicked!')} className="ml-2 cursor-pointer" />
        </span>
      </div>
      <div className="mb-80"> {/* Increased spacing */}
        <h2 className="text-xl font-semibold mb-4 mt-4">Uploaded Documents</h2>
        <ul>
          {localUploadedFiles.map((file, index) => (
            <li key={index} className="mb-2">
              {file}
            </li>
          ))}
        </ul>
      </div>
      <div className="flex flex-col justify-content:space-between items-center mt-4 gap-4 h-screen">
  <input 
    type="file" 
    id="file-upload" 
    className="hidden" 
    onChange={handleFileChangeProp} 
  />
  <label htmlFor="file-upload" className="bg-blue-500 hover:bg-blue-700 text-white text-center font-medium rounded-full px-8 py-3 shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 cursor-pointer w-64">
    Upload File
  </label>
  <button className="bg-blue-500 hover:bg-blue-700 text-white font-medium rounded-full px-8 py-3 shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 cursor-pointer w-64">
    Sign In
  </button>
</div>
    </div>
  );
};

export default ChatSidebar;