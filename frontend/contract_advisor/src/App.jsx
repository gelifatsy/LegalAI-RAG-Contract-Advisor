// import logo from './logo.svg';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Chat from './components/Chat';
import Navbar from './components/Navbar'; // Import the Navbar component

const App = () => {
  return (
    <Router>
      <Navbar /> {/* Render Navbar outside of Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Router>
  );
};

export default App;
