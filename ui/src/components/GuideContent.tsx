import React from 'react';
import { guideData } from '../data/guideData';

const GuideContent = ({ searchTerm }) => {
  const filteredData = guideData.filter(item =>
    item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="guide-content">
      {filteredData.map((item, index) => (
        <div key={index} className="guide-item">
          <h3>{item.title}</h3>
          <p>{item.content}</p>
        </div>
      ))}
    </div>
  );
};

export default GuideContent;