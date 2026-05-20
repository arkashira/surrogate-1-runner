import React, { useState } from 'react';

const FeedbackForm = ({ stepId, onSubmit }) => {
  const [feedback, setFeedback] = useState('');
  const [rating, setRating] = useState(0);
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitError('');
    
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          stepId,
          feedback,
          rating,
          email,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit feedback');
      }

      setSubmitSuccess(true);
      setFeedback('');
      setRating(0);
      setEmail('');
      
      if (onSubmit) {
        onSubmit();
      }
    } catch (error) {
      setSubmitError('Failed to submit feedback. Please try again.');
      console.error('Feedback submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="feedback-form">
      <h3>Provide Feedback on This Step</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="rating">Rating:</label>
          <div className="rating-stars">
            {[1, 2, 3, 4, 5].map((star) => (
              <span
                key={star}
                className={`star ${star <= rating ? 'filled' : ''}`}
                onClick={() => setRating(star)}
              >
                ★
              </span>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="feedback">Feedback:</label>
          <textarea
            id="feedback"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="What did you think about this step? How could it be improved?"
            required
            rows={4}
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email (optional):</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Your email address (for follow-up)"
          />
        </div>

        <button 
          type="submit" 
          disabled={isSubmitting || !feedback.trim()}
          className="submit-button"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
        </button>

        {submitSuccess && (
          <div className="success-message">
            Thank you for your feedback! It has been submitted successfully.
          </div>
        )}

        {submitError && (
          <div className="error-message">
            {submitError}
          </div>
        )}
      </form>
    </div>
  );
};

export default FeedbackForm;