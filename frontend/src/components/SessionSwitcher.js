import React, { useState } from 'react';
import PropTypes from 'prop-types';

const SessionSwitcher = ({ sessions, currentSession, switchSession }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleSessionClick = (session) => {
    switchSession(session);
    setIsDropdownOpen(false);
  };

  return (
    <div className="session-switcher">
      <button onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
        {currentSession.name} ▼
      </button>
      {isDropdownOpen && (
        <ul className="session-list">
          {sessions.map((session) => (
            <li
              key={session.id}
              className={session.id === currentSession.id ? 'active' : ''}
              onClick={() => handleSessionClick(session)}
            >
              {session.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

SessionSwitcher.propTypes = {
  sessions: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
    })
  ).isRequired,
  currentSession: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,
  switchSession: PropTypes.func.isRequired,
};

export default SessionSwitcher;