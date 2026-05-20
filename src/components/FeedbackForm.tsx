import React, { useState } from 'react';
import { storeFeedback } from '../utils/feedbackStorage';
import { analyzeFeedback } from '../utils/feedbackAnalysis';

interface FeedbackFormProps {
  onSuccess?: (result: any) => void;
  onError?: (error: any) => void;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ onSuccess, onError }) => {
  const [feedback, setFeedback] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) return;

    setSubmitting(true);
    try {
      const stored = await storeFeedback(feedback);
      const analysed = await analyzeFeedback(feedback);
      setAnalysis(analysed);
      onSuccess?.({ stored, analysed });
    } catch (err) {
      onError?.(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="feedback-form">
      <label htmlFor="feedback">
        Feedback:
        <textarea
          id="feedback"
          name="feedback"
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          required
          rows={5}
          cols={40}
        />
      </label>
      <button type="submit" disabled={submitting}>
        {submitting ? 'Submitting…' : 'Submit'}
      </button>

      {analysis && (
        <div className="feedback-analysis">
          <h4>Analysis Result</h4>
          <pre>{JSON.stringify(analysis, null, 2)}</pre>
        </div>
      )}
    </form>
  );
};

export default FeedbackForm;