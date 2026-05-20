
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SessionList = () => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    const fetchSessions = async () => {
      const response = await axios.get('/api/sessions');
      setSessions(response.data);
    };

    fetchSessions();
  }, []);

  return (
    <div>
      <h2>Active Sessions</h2>
      <ul>
        {sessions.map((session) => (
          <li key={session.id}>
            Provider: {session.provider} | Start Time: {session.startTime}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SessionList;

// src/api/sessions.js

import express from 'express';

const router = express.Router();

router.get('/', async (req, res) => {
  const sessions = await getActiveSessions();
  res.json(sessions);
});

export default router;

// src/utils/getActiveSessions.js

async function getActiveSessions() {
  // Implement the logic to fetch active sessions from the database
  // ...
}

// src/tests/__mocks__/api/sessions.js

import express from 'express';
import { getActiveSessions } from '../utils/getActiveSessions';

const router = express.Router();

router.get('/', (req, res) => {
  const sessions = [
    { id: 1, provider: 'Provider1', startTime: '2022-01-01T00:00:00' },
    { id: 2, provider: 'Provider2', startTime: '2022-01-02T00:00:00' },
  ];
  res.json(sessions);
});

export default router;

// src/tests/__mocks__/utils/getActiveSessions.js

export const getActiveSessions = () => {
  // Mock the getActiveSessions function for testing
  return Promise.resolve([
    { id: 1, provider: 'Provider1', startTime: '2022-01-01T00:00:00' },
    { id: 2, provider: 'Provider2', startTime: '2022-01-02T00:00:00' },
  ]);
};

// src/tests/SessionList.test.js

import React from 'react';
import { render, screen } from '@testing-library/react';
import SessionList from './SessionList';
import { getActiveSessions } from '../utils/getActiveSessions';
import { getServerSession } from '../api/__mocks__/api/sessions';

jest.mock('../utils/getActiveSessions');
jest.mock('../api/__mocks__/api/sessions');

describe('SessionList', () => {
  it('renders active sessions', async () => {
    getActiveSessions.mockReturnValue(Promise.resolve([
      { id: 1, provider: 'Provider1', startTime: '2022-01-01T00:00:00' },
      { id: 2, provider: 'Provider2', startTime: '2022-01-02T00:00:00' },
    ]));

    getServerSession.mockReturnValueOnce({
      json: jest.fn().mockResolvedValue([
        { id: 1, provider: 'Provider1', startTime: '2022-01-01T00:00:00' },
        { id: 2, provider: 'Provider2', startTime: '2022-01-02T00:00:00' },
      ]),
    });

    const { container } = render(<SessionList />);

    await screen.findByText('Active Sessions');
    expect(screen.getByText('Active Sessions')).toHaveClass('font-semibold');

    expect(screen.getAllByRole('listitem').length).toBe(2);
    expect(screen.getByText('Provider1')).toBeInTheDocument();
    expect(screen.getByText('Provider2')).toBeInTheDocument();
  });
});