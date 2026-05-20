import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * ProductReview component
 *
 * Props:
 *  - productId (string): ID of the product to fetch reviews for.
 *
 * Features:
 *  - Displays a list of reviews with rating, title, body, and date.
 *  - Allows filtering by relevance (default) or newest first.
 *  - Provides a form for authenticated users to submit a new review.
 *  - Refreshes the review list after a successful submission.
 */
const ProductReview = ({ productId }) => {
  const [reviews, setReviews] = useState([]);
  const [filter, setFilter] = useState('relevance'); // 'relevance' | 'date'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Form state
  const [rating, setRating] = useState(5);
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const fetchReviews = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(
        `/api/products/${productId}/reviews?sort=${filter}`
      );
      if (!res.ok) {
        throw new Error(`Error ${res.status}`);
      }
      const data = await res.json();
      setReviews(data.reviews || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await fetch(
        `/api/products/${productId}/reviews`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ rating, title, body }),
        }
      );
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.message || 'Submission failed');
      }
      // Reset form
      setRating(5);
      setTitle('');
      setBody('');
      // Refresh reviews
      fetchReviews();
    } catch (err) {
      setSubmitError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="product-review">
      <h2>Product Reviews</h2>

      {/* Filter */}
      <div className="review-filter">
        <label htmlFor="filter-select">Sort by: </label>
        <select
          id="filter-select"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="relevance">Relevance</option>
          <option value="date">Newest First</option>
        </select>
      </div>

      {/* Review List */}
      {loading ? (
        <p>Loading reviews...</p>
      ) : error ? (
        <p className="error">Error: {error}</p>
      ) : reviews.length === 0 ? (
        <p>No reviews yet.</p>
      ) : (
        <ul className="review-list">
          {reviews.map((rev) => (
            <li key={rev.id} className="review-item">
              <div className="review-header">
                <span className="review-rating">{'★'.repeat(rev.rating)}</span>
                <span className="review-title">{rev.title}</span>
                <span className="review-date">
                  {new Date(rev.created_at).toLocaleDateString()}
                </span>
              </div>
              <p className="review-body">{rev.body}</p>
            </li>
          ))}
        </ul>
      )}

      {/* Review Form */}
      <form className="review-form" onSubmit={handleSubmit}>
        <h3>Submit a Review</h3>
        {submitError && <p className="error">Error: {submitError}</p>}
        <label>
          Rating:
          <select
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
          >
            {[5, 4, 3, 2, 1].map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </label>
        <label>
          Title:
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </label>
        <label>
          Review:
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Review'}
        </button>
      </form>
    </section>
  );
};

ProductReview.propTypes = {
  productId: PropTypes.string.isRequired,
};

export default ProductReview;