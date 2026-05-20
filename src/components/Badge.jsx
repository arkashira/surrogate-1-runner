import React from 'react';

export const Badge = ({ status, children, className = '' }) => {
  const statusClasses = {
    ready: 'badge-success',
    pending: 'badge-warning', 
    error: 'badge-error',
    complete: 'badge-success'
  };
  
  return (
    <span className={`badge ${statusClasses[status] || 'badge-default'} ${className}`}>
      {children}
    </span>
  );
};