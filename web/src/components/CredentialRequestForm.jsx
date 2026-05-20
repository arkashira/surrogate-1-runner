import React, { useState } from 'react';
import axios from 'axios';

const CredentialRequestForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [skillArea, setSkillArea] = useState('');
  const [requestId, setRequestId] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!name || !email || !skillArea) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      const response = await axios.post('/api/credential-requests', {
        name,
        email,
        skillArea,
      });
      setRequestId(response.data.requestId);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name:
        <input type="text" value={name} onChange={(event) => setName(event.target.value)} />
      </label>
      <br />
      <label>
        Email:
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
      </label>
      <br />
      <label>
        Skill Area:
        <input type="text" value={skillArea} onChange={(event) => setSkillArea(event.target.value)} />
      </label>
      <br />
      <button type="submit">Submit</button>
      {requestId && <p>Request ID: {requestId}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
};

export default CredentialRequestForm;