import React from 'react';
import { render, screen } from '@testing-library/react';
import VariantComparisonCard from './VariantComparisonCard';
import { Variant } from '../types';

const mockVariant: Variant = {
  id: '1',
  name: 'Variant 1',
  openaiCompatibility: 'full',
  modelContextProtocolVersion: '1.0',
  containerizationRequirements: ['Docker'],
  harnessPatternType: 'serverless',
};

describe('VariantComparisonCard', () => {
  it('renders the variant name', () => {
    render(<VariantComparisonCard variant={mockVariant} />);
    expect(screen.getByText('Variant 1')).toBeInTheDocument();
  });

  it('displays the OpenAI compatibility status', () => {
    render(<VariantComparisonCard variant={mockVariant} />);
    expect(screen.getByText('OpenAI Compatibility:')).toBeInTheDocument();
    expect(screen.getByText('full')).toBeInTheDocument();
  });

  it('displays the Model Context Protocol version', () => {
    render(<VariantComparisonCard variant={mockVariant} />);
    expect(screen.getByText('Model Context Protocol Version: 1.0')).toBeInTheDocument();
  });

  it('displays the containerization requirements', () => {
    render(<VariantComparisonCard variant={mockVariant} />);
    expect(screen.getByText('Containerization Requirements: Docker')).toBeInTheDocument();
  });

  it('displays the harness pattern type', () => {
    render(<VariantComparisonCard variant={mockVariant} />);
    expect(screen.getByText('Harness Pattern Type: serverless')).toBeInTheDocument();
  });
});