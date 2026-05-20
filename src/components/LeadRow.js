import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';
import { moveToNextStage, getLeadHistory } from '../api/lead';

const LeadRow = ({ lead, stages, onStageChange }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState(lead.stageHistory || []);

  const currentIndex = stages.indexOf(lead.stage);
  const isLastStage = currentIndex === stages.length - 1;

  const handleMoveToNextStage = async () => {
    if (isLastStage) return;

    setLoading(true);
    setError(null);

    try {
      // Move lead to next stage
      const updatedLead = await moveToNextStage(lead.id);

      // Update history
      const newHistory = await getLeadHistory(lead.id);
      setHistory(newHistory);

      // Notify parent component
      onStageChange(updatedLead);
    } catch (err) {
      setError(err.message || 'Failed to move lead');
      console.error('Error moving lead:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="lead-row">
      <h2>{lead.name}</h2>
      <p>Stage: {lead.stage}</p>

      {history.length > 0 && (
        <details>
          <summary>Stage History</summary>
          <ul>
            {history.map((h, idx) => (
              <li key={idx}>
                {h.from} → {h.to} @ {new Date(h.timestamp).toLocaleString()}
              </li>
            ))}
          </ul>
        </details>
      )}

      <Button
        onClick={handleMoveToNextStage}
        disabled={loading || isLastStage}
        variant={isLastStage ? 'secondary' : 'primary'}
      >
        {loading ? 'Processing...' : isLastStage ? 'Final Stage' : 'Move to Next Stage'}
      </Button>

      {error && <div className="text-danger mt-2">{error}</div>}
    </div>
  );
};

LeadRow.propTypes = {
  lead: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    name: PropTypes.string.isRequired,
    stage: PropTypes.string.isRequired,
    stageHistory: PropTypes.arrayOf(
      PropTypes.shape({
        from: PropTypes.string.isRequired,
        to: PropTypes.string.isRequired,
        timestamp: PropTypes.string.isRequired,
      })
    ),
  }).isRequired,
  stages: PropTypes.arrayOf(PropTypes.string).isRequired,
  onStageChange: PropTypes.func.isRequired,
};

export default LeadRow;