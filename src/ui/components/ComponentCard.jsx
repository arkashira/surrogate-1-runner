import React from 'react';
import StarRatings from 'react-star-ratings';

const ComponentCard = ({ component }) => {
  const { ratings = { average: 0, count: 0 }, comments = [] } = component;

  const topComments = comments
    .sort((a, b) => b.helpfulCount - a.helpfulCount)
    .slice(0, 3);

  return (
    <div className="component-card">
      {/* Existing component content */}
      <h2>{component.name}</h2>
      <p>{component.description}</p>

      {/* New rating widget */}
      <div className="rating-widget">
        {ratings.count > 0 ? (
          <>
            <div className="rating-header">
              <StarRatings
                rating={ratings.average}
                starRatedColor="#f97316"
                starEmptyColor="#e5e7eb"
                starDimension="20px"
                starSpacing="2px"
                numberOfStars={5}
                name="rating"
              />
              <span className="rating-count">
                ({ratings.count} ratings)
              </span>
            </div>
            <div className="top-comments">
              {topComments.map((comment, idx) => (
                <div key={idx} className="comment">
                  <p className="comment-text">{comment.text}</p>
                  <span className="helpful-count">
                    {comment.helpfulCount} found helpful
                  </span>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="no-reviews">
            <p>No community reviews yet for this component</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ComponentCard;