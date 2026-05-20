import React, { useState } from 'react';

/**
 * FeedbackForm component
 *
 * Provides a simple, accessible feedback form that can be toggled
 * open/closed. Submits data to the `/api/feedback` endpoint.
 */
const FeedbackForm = () => {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState('');

  const submit = async (e) => {
    e.preventDefault();
    setStatus('Submitting...');
    try {
      const res = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message })
      });
      if (res.ok) {
        setStatus('Thank you for your feedback!');
        setName('');
        setEmail('');
        setMessage('');
      } else {
        setStatus('Error submitting feedback.');
      }
    } catch (err) {
      setStatus('Network error.');
    }
  };

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        aria-label="Toggle feedback form"
        style={{ marginBottom: '1rem' }}
      >
        {open ? 'Close Feedback' : 'Give Feedback'}
      </button>
      {open && (
        <form onSubmit={submit} aria-label="Feedback form">
          <div>
            <label htmlFor="feedback-name">Name:</label>
            <input
              id="feedback-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="feedback-email">Email:</label>
            <input
              id="feedback-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="feedback-message">Message:</label>
            <textarea
              id="feedback-message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
            />
          </div>
          <button type="submit">Submit</button>
          {status && <p>{status}</p>}
        </form>
      )}
    </div>
  );
};

export default FeedbackForm;