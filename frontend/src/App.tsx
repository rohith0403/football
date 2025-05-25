import React from 'react';
import { Route, BrowserRouter as Router, Routes, useNavigate } from 'react-router-dom';
import Players from './components/Players'; // Adjust the import path as necessary
import Teams from './components/Teams'; // Adjust the import path as necessarys


/**
 * HomePage Component
 * Displays the welcome message for the Football Sim.
 */
const HomePage: React.FC = () => {
  return (
    <div className="text-center text-gray-300 text-lg p-6 bg-gray-700 rounded-lg">
      <p className="mb-4">Welcome to your Football Simulation Hub!</p>
      <p>Navigate using the buttons above or to the left to manage players and teams.</p>
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

  // useNavigate is still used for the "Reset Database" button as it performs an action
  // that also involves navigation, but it's not a direct link to a content page.
  const navigate = useNavigate();

  return (
    // The outermost container sets up the full screen background and centers its content.
    // It now contains the main app frame (sidebar) and the routed content as siblings.
    <div className="min-h-screen bg-gray-900 flex flex-col md:flex-row p-4 font-sans">
      {/* Main App Frame: Contains the title and sidebar */}
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700 md:w-1/4 lg:w-1/5 mb-10 md:mb-0 md:mr-10 flex flex-col items-center">

        {/* Title for smaller screens (hidden on medium and larger screens). */}
        <h1 className="text-5xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 mb-10 drop-shadow-lg md:hidden">
          Welcome to Football Sim
        </h1>

        {/* Title for medium and larger screens (hidden on small screens). */}
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 mb-6 drop-shadow-lg hidden md:block">
          Football Sim
        </h1>

        {/* Sidebar Navigation Buttons */}
        <div className="flex flex-wrap justify-center gap-6 md:flex-col w-full">
          {/* Reset Database Button - remains a button as it's an action */}
          <button
            onClick={() => {
              navigate('/');
            }}
            className="flex items-center justify-center px-6 py-3 bg-transparent text-gray-400 font-medium text-base rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-opacity-75 transition duration-300 ease-in-out w-full md:w-auto"
          >
            Home
          </button>

          {/* View Players Link - now an <a> tag with simplified styling */}
          <a
            href="/players" // Use href for navigation
            className={`flex items-center justify-center px-6 py-3 font-medium text-base rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-75 transition duration-300 ease-in-out w-full md:w-auto ${window.location.pathname === '/players'
              ? 'bg-blue-700 text-white'
              : 'bg-transparent text-gray-400 hover:bg-gray-700'
              }`}
          >
            View Players
          </a>

          {/* View Teams Link - now an <a> tag with simplified styling */}
          <a
            href="/teams" // Use href for navigation
            className={`flex items-center justify-center px-6 py-3 font-medium text-base rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-75 transition duration-300 ease-in-out w-full md:w-auto ${window.location.pathname === '/teams'
              ? 'bg-blue-700 text-white'
              : 'bg-transparent text-gray-400 hover:bg-gray-700'
              }`}
          >
            View Teams
          </a>
        </div>
      </div>

      {/* The Routes component is now a sibling, allowing it to render full-page components */}
      <div className="flex-1 flex items-center justify-center"> {/* Added flex-1 and centering for routed content */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/players" element={<Players />} />

          <Route path="*" element={<div className="text-center text-red-400 text-xl font-medium py-8">404 - Page Not Found</div>} />
        </Routes>
      </div>
    </div>
  );
};

const RootApp: React.FC = () => (
  <Router>
    <App />
  </Router>
);

export default RootApp;
