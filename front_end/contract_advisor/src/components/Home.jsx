// import React from 'react';
import { Link } from 'react-router-dom'



const Home = () => {
const backgroundStyle = {
        backgroundImage: 'url("/home/elias/Pictures/lizzy_background.png")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      };
  return (
    <div className="home-container flex flex-col items-center justify-center bg-white w-full pt-20"style={backgroundStyle}>
             <h1 className="home-title text-7xl font-bold text-center text-gray-800 leading-tight mb-12">
        Your AI Contract<br />Assistant
      </h1>
      <p className="home-description text-xl text-center text-gray-600 mt-4">
        The next generation contract AI, right in Microsoft Word. Draft<br/> and review contracts better and faster!
      </p>
      <div className="button-container mt-8">
        <Link to="/chat">
        <button
          className="home-button bg-blue-500 text-white font-medium rounded-full px-6 py-3 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-lg" // Use shadow-lg for a stronger shadow
          style={{
            boxShadow: '0 10px 15px rgba(0, 0, 0, 0.15)', // Add custom box-shadow for 3D effect
          }}
        >
          Try Our Product
        </button>
        </Link>
      </div>
    </div>
  );
};

export default Home;



