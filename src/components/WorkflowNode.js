import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './workflowNode.css';

const WorkflowNode = ({ id, title, description, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={`workflow-node ${isHovered ? 'hovered' : ''}`}
      onClick={() => onClick(id)}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="node-header">
        <h3>{title}</h3>
      </div>
      {isHovered && (
        <div className="node-info">
          <p>{description}</p>
        </div>
      )}
    </div>
  );
};

WorkflowNode.propTypes = {
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default WorkflowNode;