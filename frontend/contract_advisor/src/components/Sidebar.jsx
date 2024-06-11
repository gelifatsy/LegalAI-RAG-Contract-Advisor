// Sidebar.jsx
// import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="sidebar-container bg-blue-500 text-white p-4">
      <h2 className="text-xl font-bold mb-4">Services</h2>
      <ul className="mb-4">
        <li>Service 1</li>
        <li>Service 2</li>
        <li>Service 3</li>
        {/* Add more services as needed */}
      </ul>
      <Link to="/upload">
        <button className="bg-white text-blue-500 font-medium rounded-full px-4 py-2 hover:bg-blue-100 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Upload File</button>
      </Link>
    </div>
  );
};

export default Sidebar;
