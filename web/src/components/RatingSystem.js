import React from 'react';
import axios from 'axios';

const RatingSystem = ({ caseStudyId }) => {
  const handleRating = async (rating) => {
    try {
      await axios.post(`/api/case-studies/${caseStudyId}/rate`, { rating });
      console.log(`Rated ${caseStudyId} with ${rating}`);
    } catch (error) {
      console.error('Error rating case study:', error);
    }
  };

  return (
    <div>
      {[1, 2, 3, 4, 5].map((star) => (
        <button key={star} onClick={() => handleRating(star)}>
          {star}
        </button>
      ))}
    </div>
  );
};

export default RatingSystem;