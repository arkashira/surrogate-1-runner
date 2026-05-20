import React, { useState, useEffect } from 'react';
import { filterReviews } from '../utils/validation';

const CommunityReview = ({ componentId }) => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual endpoint
        const response = await fetch(`/api/components/${componentId}/reviews`);
        if (!response.ok) throw new Error('Failed to fetch reviews');
        
        const data = await response.json();
        const approvedReviews = filterReviews(data.reviews);
        setReviews(approvedReviews);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [componentId]);

  if (loading) return <div className="loading">Loading reviews...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="community-reviews">
      <h2>Community Reviews</h2>
      {reviews.length === 0 ? (
        <p>No reviews available yet.</p>
      ) : (
        <div className="reviews-list">
          {reviews.map(review => (
            <div key={review.id} className="review-card">
              <div className="review-header">
                <span className="user-id">{review.userId}</span>
                <div className="rating">
                  {'★'.repeat(review.rating)}{'☆'.repeat(MAX_RATING - review.rating)}
                </div>
              </div>
              <p className="review-comment">{review.comment}</p>
              <div className="review-meta">
                <span className="review-date">{new Date(review.date).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CommunityReview;