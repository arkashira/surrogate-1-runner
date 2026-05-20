import React, { useState } from 'react';

interface FeedbackFormProps {
  onSubmit: (feedback: string) => void;
}

export const FeedbackForm: React.FC<FeedbackFormProps> = ({ onSubmit }) => {
  const [feedback, setFeedback] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(feedback);
    setFeedback('');
  };

  return (
    <form onSubmit={handleSubmit} className="feedback-form">
      <h2>Provide Feedback</h2>
      <textarea
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        placeholder="Enter your feedback here..."
        required
      />
      <button type="submit">Submit Feedback</button>
    </form>
  );
};