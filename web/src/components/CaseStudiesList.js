import React from 'react';

const CaseStudiesList = ({ caseStudies }) => {
  return (
    <div>
      {caseStudies.map((study, index) => (
        <div key={index}>
          <h3>{study.title}</h3>
          <p>{study.description}</p>
          <p>Approach: {study.approach}</p>
          <p>Results: {study.results}</p>
        </div>
      ))}
    </div>
  );
};

export default CaseStudiesList;