import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Players from './components/Players';
import Teams from './components/Teams';


/**
 * HomePage Component
 * Displays the welcome message for the Football Sim.
 */
const HomePage: React.FC = () => {
  return (
    <div className="text-center text-gray-300 text-lg p-6 bg-gray-700 rounded-lg">
      <p className="mb-4">Welcome to your Football Simulation Hub!</p>
      <p>Navigate using the buttons above to manage players and teams.</p>
      <p className="mt-4 text-sm text-gray-400">
        Explore player statistics or view team details.
      </p>
    </div>
  );
};


/**
 * Main App Component
 * Integrates routing, data management, and navigation.
 */
const App: React.FC = () => {

  const navigate = useNavigate(); // Hook for programmatic navigation

  return (
    // Wrap the entire application content with Router for routing to work
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black flex items-center justify-center p-4 font-sans">
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-screen-lg border border-gray-700">
        <h1 className="text-5xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 mb-10 drop-shadow-lg">
          Welcome to Football Sim
        </h1>

        {/* Navigation Buttons */}
        <div className="flex flex-wrap justify-center gap-6 mb-10">
          <button
            onClick={() => {
              navigate('/'); // Navigate to home after reset
            }}
            className="flex items-center px-8 py-4 bg-gradient-to-r from-red-700 to-red-900 text-white font-bold text-lg rounded-full shadow-lg hover:from-red-800 hover:to-red-950 focus:outline-none focus:ring-4 focus:ring-red-600 focus:ring-opacity-75 transition duration-300 ease-in-out transform hover:scale-105"
          >
            {/* Database Reset Icon */}
            <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 7v10c0 .552.448 1 1 1h14c.552 0 1-.448 1-1V7m-4 0V4a2 2 0 00-2-2H8a2 2 0 00-2 2v3m4 0h4m-4 0h.01M9 12h.01M15 12h.01M9 16h.01M15 16h.01"></path>
            </svg>
            Reset Database
          </button>
          <button
            onClick={() => navigate('/players')} // Navigate to /players route
            className={`flex items-center px-8 py-4 font-bold text-lg rounded-full shadow-lg focus:outline-none focus:ring-4 focus:ring-blue-600 focus:ring-opacity-75 transition duration-300 ease-in-out transform hover:scale-105 ${
              window.location.pathname === '/players'
                ? 'bg-gradient-to-r from-blue-600 to-blue-800 text-white'
                : 'bg-gradient-to-r from-blue-800 to-blue-900 text-gray-200 hover:from-blue-700 hover:to-blue-850'
            }`}
          >
            {/* Player Icon (User) */}
            <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            View Players
          </button>
          <button
            onClick={() => navigate('/teams')} // Navigate to /teams route
            className={`flex items-center px-8 py-4 font-bold text-lg rounded-full shadow-lg focus:outline-none focus:ring-4 focus:ring-blue-600 focus:ring-opacity-75 transition duration-300 ease-in-out transform hover:scale-105 ${
              window.location.pathname === '/teams'
                ? 'bg-gradient-to-r from-blue-600 to-blue-800 text-white'
                : 'bg-gradient-to-r from-blue-800 to-blue-900 text-gray-200 hover:from-blue-700 hover:to-blue-850'
            }`}
          >
            {/* Team Icon (Users Group) */}
            <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h2a2 2 0 002-2V7a2 2 0 00-2-2h-3v4l-3-3-3 3V5H5a2 2 0 00-2 2v11a2 2 0 002 2h2M12 14a7 7 0 00-7 7h14a7 7 0 00-7-7zm-4 0v-2a4 4 0 014-4h0a4 4 0 014 4v2m-4-2h.01"></path>
            </svg>
            View Teams
          </button>
        </div>

        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* <Route path="/players" element={<PlayersPage players={players} initializeData={initializeData} />} /> */}
          <Route path="/teams" element={<Teams/>} />
          <Route path="/players" element={<Players/>} />
          
          {/* Fallback for any unmatched routes */}
          <Route path="*" element={<div className="text-center text-red-400 text-xl font-medium py-8">404 - Page Not Found</div>} />
        </Routes>
      </div>
    </div>
  );
};

// Main component that wraps App with Router. This is crucial for routing to work.
// In a typical React setup, this would be in index.tsx or main.tsx.
// For self-contained immersive, we'll nest it here.
const RootApp: React.FC = () => (
  <Router>
    <App />
  </Router>
);

export default RootApp;
