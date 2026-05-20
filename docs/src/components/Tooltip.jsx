import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  shouldShowTooltip,
  dismissTooltip,
} from '../utils/tooltipUtils';

const Tooltip = ({ featureId, docs }) => {
  const [visible, setVisible] = useState(false);
  const doc = docs[featureId];

  useEffect(() => {
    if (!doc) return;
    if (shouldShowTooltip(featureId)) {
      setVisible(true);
    }
  }, [featureId, doc]);

  const handleDismiss = () => {
    dismissTooltip(featureId);
    setVisible(false);
  };

  if (!visible || !doc) return null;

  return (
    <div className="tooltip">
      <p>{doc.description}</p>
      <Link to={doc.link} className="tooltip-link">
        Learn more
      </Link>
      <button onClick={handleDismiss} className="tooltip-dismiss">
        Dismiss
      </button>
    </div>
  );
};

export default Tooltip;