import React from 'react';
import PropTypes from 'prop-types';

/**
 * RecommendationList
 *
 * Displays a ranked list of upgrade recommendations.
 *
 * Props:
 * - recommendations: Array of objects with keys:
 *   - id: unique identifier
 *   - rank: integer (1-3)
 *   - componentName: string
 *   - price: number (USD)
 *   - expectedFPS: number
 *   - roi: number (percentage)
 * - onSelect: function(recommendationId) called when user clicks Select
 * - loading: boolean indicating data is being fetched
 * - error: string error message to display
 */
const RecommendationList = ({
  recommendations,
  onSelect,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div data-testid="loading" className="recommendation-list-loading">
        Loading recommendations...
      </div>
    );
  }

  if (error) {
    return (
      <div data-testid="error" className="recommendation-list-error">
        {error}
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div data-testid="no-results" className="recommendation-list-no-results">
        No upgrade recommendations found for the selected configuration.
      </div>
    );
  }

  return (
    <table data-testid="recommendation-table" className="recommendation-list-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Component</th>
          <th>Price (USD)</th>
          <th>Expected FPS</th>
          <th>ROI (%)</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {recommendations.slice(0, 3).map((rec) => (
          <tr key={rec.id}>
            <td>{rec.rank}</td>
            <td>{rec.componentName}</td>
            <td>{rec.price.toFixed(2)}</td>
            <td>{rec.expectedFPS}</td>
            <td>{rec.roi.toFixed(1)}</td>
            <td>
              <button
                type="button"
                onClick={() => onSelect(rec.id)}
                data-testid={`select-btn-${rec.id}`}
              >
                Select
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

RecommendationList.propTypes = {
  recommendations: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      rank: PropTypes.number.isRequired,
      componentName: PropTypes.string.isRequired,
      price: PropTypes.number.isRequired,
      expectedFPS: PropTypes.number.isRequired,
      roi: PropTypes.number.isRequired,
    })
  ),
  onSelect: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  error: PropTypes.string,
};

RecommendationList.defaultProps = {
  recommendations: [],
  loading: false,
  error: '',
};

export default RecommendationList;