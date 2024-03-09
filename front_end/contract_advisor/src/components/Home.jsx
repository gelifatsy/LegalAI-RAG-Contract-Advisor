// import React from 'react';
import lizzy_background from '../assets/lizzy_background.png';
import { Link } from 'react-router-dom';

const Home = () => {
  const containerStyle = {
    backgroundImage: `url(${lizzy_background})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center center',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'flex-start', // Align content at the start of the container
    textAlign: 'center',
    padding: '10px',
    minHeight: '70vh',
  };
  

  const contentStyle = {
    marginTop: '0', // Adjust as needed
  };

  return (
    <div className="home-container relative flex flex-col items-center justify-center bg-white w-full pt-20">
      <h1 className="home-title text-7xl font-bold text-gray-800 leading-tight mb-12">
        Your AI Contract<br />Assistant
      </h1>
      <div style={containerStyle}>
        <div style={contentStyle}>
          <p className="home-description text-xl text-gray-600 w-full"  style={{ marginTop: '0' }}>
            The next generation contract AI, right in Microsoft Word. Draft<br/> and review contracts better and faster!
          </p>
          <div className="button-container mt-8" style={{ marginTop: '0' }}>
            <Link to="/chat">
              <button
                className="home-button bg-blue-500 text-white font-medium rounded-full px-6 py-3 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-lg"
              >
                Try Our Product
              </button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
