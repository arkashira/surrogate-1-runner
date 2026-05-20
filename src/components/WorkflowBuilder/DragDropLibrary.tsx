import React, { useState } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { ItemTypes } from './ItemTypes';

const DragDropLibrary = ({ components, onDrop }) => {
  const [selectedComponent, setSelectedComponent] = useState(null);

  const [{ isDragging }, drag] = useDrag({
    type: ItemTypes.COMPONENT,
    item: { type: ItemTypes.COMPONENT, id: selectedComponent },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  const [, drop] = useDrop({
    accept: ItemTypes.COMPONENT,
    drop: (item) => onDrop(item.id),
  });

  return (
    <div className="drag-drop-library" ref={(node) => drag(drop(node))}>
      <h2>Components</h2>
      <div className="components-list">
        {components.map((component) => (
          <div
            key={component.id}
            className={`component-item ${selectedComponent === component.id ? 'selected' : ''}`}
            onClick={() => setSelectedComponent(component.id)}
            style={{ opacity: isDragging ? 0.5 : 1 }}
          >
            {component.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DragDropLibrary;