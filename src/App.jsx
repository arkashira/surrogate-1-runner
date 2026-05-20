import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WholphinDashboard from './components/WholphinDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard/wholphin" element={<WholphinDashboard />} />
        {/* Add more routes here */}
      </Routes>
    </Router>
  );
}

export default App;