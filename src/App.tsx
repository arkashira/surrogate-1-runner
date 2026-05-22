import React from 'react';
import ComparisonTable from './components/ComparisonTable';
import { ClawVariant } from './types';

const variants: ClawVariant[] = [
  {
    id: '1',
    name: 'Variant A',
    capabilities: {
      'Feature X': true,
      'Feature Y': false,
      'Feature Z': true,
    },
  },
  {
    id: '2',
    name: 'Variant B',
    capabilities: {
      'Feature X': false,
      'Feature Y': true,
      'Feature Z': true,
    },
  },
];

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Claw Variant Comparison</h1>
      <ComparisonTable variants={variants} />
    </div>
  );
};

export default App;