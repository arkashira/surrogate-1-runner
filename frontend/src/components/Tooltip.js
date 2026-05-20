import React from 'react';

const Tooltip = ({ children, text }) => {
  return (
    <span>
      {children}
      <span className="tooltip">{text}</span>
    </span>
  );
};

export default Tooltip;