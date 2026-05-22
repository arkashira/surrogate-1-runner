import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ApiKeys = () => {
  const [apiKeys, setApiKeys] = useState([]);
  const [newApiKey, setNewApiKey] = useState('');
  const [concurrentStreams, setConcurrentStreams] = useState(10);
  const [apiKeyStatus, setApiKeyStatus] = useState('');

  useEffect(() => {
    fetchApiKeys();
  }, []);

  const fetchApiKeys = async () => {
    try {
      const response = await axios.get('/api/api-keys');
      setApiKeys(response.data);
    } catch (error) {
      console.error('Error fetching API keys:', error);
    }
  };

  const handleCreateApiKey = async () => {
    try {
      const response = await axios.post('/api/api-keys', {
        apiKey: newApiKey,
        concurrentStreams: concurrentStreams,
      });
      setApiKeys([...apiKeys, response.data]);
      setNewApiKey('');
      setConcurrentStreams(10);
      setApiKeyStatus('API key created successfully.');
    } catch (error) {
      setApiKeyStatus('Error creating API key.');
      console.error('Error creating API key:', error);
    }
  };

  return (
    <div>
      <h1>API Key Management</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <label>
          New API Key:
          <input
            type="text"
            value={newApiKey}
            onChange={(e) => setNewApiKey(e.target.value)}
          />
        </label>
        <br />
        <label>
          Concurrent Streams:
          <select
            value={concurrentStreams}
            onChange={(e) => setConcurrentStreams(Number(e.target.value))}
          >
            <option value="10">10</option>
            <option value="50">50</option>
            <option value="200">200</option>
          </select>
        </label>
        <br />
        <button onClick={handleCreateApiKey}>Create API Key</button>
      </form>
      <p>{apiKeyStatus}</p>
      <h2>Existing API Keys</h2>
      <ul>
        {apiKeys.map((apiKey, index) => (
          <li key={index}>
            {apiKey.apiKey} - {apiKey.concurrentStreams} concurrent streams
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ApiKeys;