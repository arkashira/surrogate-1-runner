import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProjectList from './pages/validation/ProjectList';
import ProjectDetail from './pages/validation/ProjectDetail'; // assumed existing

const App = () => (
  <Router>
    <Routes>
      <Route path="/validation" element={<ProjectList />} />
      <Route path="/validation/project/:id" element={<ProjectDetail />} />
    </Routes>
  </Router>
);

export default App;