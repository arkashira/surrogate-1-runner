import React from 'react';
import './ComponentList.css';

const ComponentList = ({ components }) => {
  return (
    <div className="component-list-container">
      {components.map((component) => (
        <div key={component.name} className="component-list-item">
          <h2>{component.name}</h2>
          <p>Price: {component.price}</p>
          <p>Specs: {component.specs}</p>
        </div>
      ))}
    </div>
  );
};

export default ComponentList;