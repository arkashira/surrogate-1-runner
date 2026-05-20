import React from 'react';
import AlternativesComparison from './AlternativesComparison';
import AlternativesList from './AlternativesList';

interface Props {
  alternatives: { name: string; performance: number; price: number }[];
}

const AlternativesComparisonContainer = ({ alternatives }: Props) => {
  return (
    <div>
      <AlternativesComparison alternatives={alternatives} />
      <AlternativesList alternatives={alternatives} />
    </div>
  );
};

export default AlternativesComparisonContainer;