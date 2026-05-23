import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import DashboardLandingPage from './components/DashboardLandingPage';
import LoginPage from './components/LoginPage';

const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/dashboard" element={<DashboardLandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          {/* Add more routes here */}
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;