import React from 'react';
import { Provider } from 'react-redux';
import { store } from './app/store';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SandboxStatus from './features/sandbox/SandboxStatus';

const SandboxPage = () => <h1>Sandbox Home</h1>; // placeholder

const App: React.FC = () => (
  <Provider store={store}>
    <Router>
      <Routes>
        <Route path="/" element={<SandboxStatus />} />
        <Route path="/sandbox" element={<SandboxPage />} />
      </Routes>
    </Router>
  </Provider>
);

export default App;