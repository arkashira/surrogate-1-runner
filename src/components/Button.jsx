import React from 'react';

export const Button = ({ 
  onClick, 
  disabled = false, 
  variant = 'primary',
  children, 
  type = 'button',
  className = ''
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant} ${className}`}
    >
      {children}
    </button>
  );
};