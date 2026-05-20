import React from 'react';

interface OverlayProps {
  children: React.ReactNode;
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
}

const Overlay: React.FC<OverlayProps> = ({ children, position }) => {
  const positionStyle: React.CSSProperties = {
    position: 'absolute',
    padding: '10px',
    backgroundColor: 'white',
    borderRadius: '5px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    zIndex: 1000,
  };

  switch (position) {
    case 'top-left':
      positionStyle.top = '10px';
      positionStyle.left = '10px';
      break;
    case 'top-right':
      positionStyle.top = '10px';
      positionStyle.right = '10px';
      break;
    case 'bottom-left':
      positionStyle.bottom = '10px';
      positionStyle.left = '10px';
      break;
    case 'bottom-right':
      positionStyle.bottom = '10px';
      positionStyle.right = '10px';
      break;
    default:
      break;
  }

  return <div style={positionStyle}>{children}</div>;
};

export default Overlay;