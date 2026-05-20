import React, { useState } from 'react';
import { useDrop } from 'react-dnd';
import { ItemTypes } from './ItemTypes';

const Canvas = () => {
  const [components, setComponents] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const [, drop] = useDrop({
    accept: ItemTypes.COMPONENT,
    drop: (item, monitor) => {
      const delta = monitor.getClientOffset();
      const left = delta.x;
      const top = delta.y;
      setComponents([...components, { id: item.id, left, top }]);
    },
  });

  const handleZoom = (delta) => {
    setZoom(Math.max(0.5, Math.min(2, zoom + delta)));
  };

  const handlePan = (deltaX, deltaY) => {
    setPosition({ x: position.x + deltaX, y: position.y + deltaY });
  };

  return (
    <div
      className="canvas"
      ref={drop}
      style={{
        transform: `scale(${zoom}) translate(${position.x}px, ${position.y}px)`,
        width: '100%',
        height: '100%',
        position: 'relative',
      }}
      onWheel={(e) => {
        e.preventDefault();
        handleZoom(e.deltaY > 0 ? -0.1 : 0.1);
      }}
      onMouseDown={(e) => {
        const startX = e.clientX;
        const startY = e.clientY;

        const onMouseMove = (e) => {
          const deltaX = e.clientX - startX;
          const deltaY = e.clientY - startY;
          handlePan(deltaX, deltaY);
        };

        const onMouseUp = () => {
          document.removeEventListener('mousemove', onMouseMove);
          document.removeEventListener('mouseup', onMouseUp);
        };

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
      }}
    >
      {components.map((component) => (
        <div
          key={component.id}
          className="component"
          style={{
            position: 'absolute',
            left: component.left,
            top: component.top,
            width: '100px',
            height: '100px',
            backgroundColor: 'lightblue',
          }}
        >
          {component.id}
        </div>
      ))}
    </div>
  );
};

export default Canvas;