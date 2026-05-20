const PROFANITY_FILTER = new Set(['spam', 'fake', 'hate', 'violence']);
const MIN_RATING = 1;
const MAX_RATING = 5;
const MIN_REVIEW_LENGTH = 10;

export function validateReview(review) {
  if (!review || typeof review !== 'object') return false;
  
  // Check required fields
  if (!review.id || !review.userId || !review.componentId || !review.rating || !review.comment) {
    return false;
  }
  
  // Validate rating range
  if (review.rating < MIN_RATING || review.rating > MAX_RATING) {
    return false;
  }
  
  // Validate comment length
  if (review.comment.length < MIN_REVIEW_LENGTH) {
    return false;
  }
  
  // Check for profanity
  const lowerComment = review.comment.toLowerCase();
  for (const word of PROFANITY_FILTER) {
    if (lowerComment.includes(word)) {
      return false;
    }
  }
  
  return true;
}

export function moderateReview(review) {
  if (!validateReview(review)) {
    return { status: 'rejected', reason: 'validation_failed' };
  }
  
  // Check for suspicious patterns
  if (review.rating === MAX_RATING && review.comment.length < 20) {
    return { status: 'pending', reason: 'suspicious_high_rating' };
  }
  
  if (review.comment.includes('best ever') || review.comment.includes('perfect')) {
    return { status: 'pending', reason: 'generic_praise' };
  }
  
  return { status: 'approved', reason: 'valid_review' };
}

export function filterReviews(reviews) {
  return reviews.filter(review => {
    const moderation = moderateReview(review);
    return moderation.status === 'approved';
  });
}