import React from 'react';
import { Link } from 'react-router-dom';

const Homepage = () => {
  return (
    <div className="homepage">
      <h1>Welcome to Axentx</h1>
      <nav>
        <ul>
          <li><Link to="/dashboard">Dashboard</Link></li>
          <li><Link to="/settings">Settings</Link></li>
          <li><Link to="/terminal">Terminal</Link></li>
          <li><Link to="/docs/shell_quickstart.md">Shell Access Quick Start Guide</Link></li>
        </ul>
      </nav>
    </div>
  );
};

export default Homepage;