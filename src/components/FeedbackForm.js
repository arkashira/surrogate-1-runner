import React, { useState } from 'react';
import axios from 'axios';
import './FeedbackForm.css';

const FeedbackForm = () => {
  const [feedback, setFeedback] = useState('');
  const [rating, setRating] = useState(0);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('/api/feedback', { feedback, rating });
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <div className="feedback-form">
      {!submitted ? (
        <form onSubmit={handleSubmit}>
          <label>
            Your Feedback:
            <textarea value={feedback} onChange={(e) => setFeedback(e.target.value)} />
          </label>
          <br />
          <label>
            Rating:
            <input type="number" min="1" max="5" value={rating} onChange={(e) => setRating(e.target.value)} />
          </label>
          <br />
          <button type="submit">Submit</button>
        </form>
      ) : (
        <p>Thank you for your feedback!</p>
      )}
    </div>
  );
};

export default FeedbackForm;