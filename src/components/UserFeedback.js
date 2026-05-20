import React, { useState } from 'react';
import { logEvent } from '../analytics/tracking';

const UserFeedback = () => {
  const [feedback, setFeedback] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    logEvent('UserFeedback', 'Submit', feedback);
    // TODO: Send feedback to backend
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Feedback:
        <input type="text" value={feedback} onChange={(e) => setFeedback(e.target.value)} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default UserFeedback;