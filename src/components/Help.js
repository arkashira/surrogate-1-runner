import React from 'react';
import './Help.css';

const Help = () => {
  return (
    <div className="help-container">
      <h1>Need Help?</h1>
      <p>Explore our resources to assist you in using the platform effectively.</p>
      <div className="help-links">
        <a href="/faq">FAQ</a>
        <a href="/support">Contact Support</a>
        <a href="/guides">User Guides</a>
      </div>
    </div>
  );
};

export default Help;