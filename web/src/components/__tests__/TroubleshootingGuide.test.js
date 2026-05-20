import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TroubleshootingGuide from '../TroubleshootingGuide';

describe('TroubleshootingGuide component', () => {
  test('renders the guide title', () => {
    render(<TroubleshootingGuide />);
    expect(
      screen.getByRole('heading', { name: /CFD Simulation Troubleshooting Guide/i })
    ).toBeInTheDocument();
  });

  test('renders at least one error section with steps', () => {
    render(<TroubleshootingGuide />);
    const meshSection = screen.getByRole('heading', { name: /Mesh Quality Issues/i });
    expect(meshSection).toBeInTheDocument();

    // Verify that a known step is present
    expect(screen.getByText(/Check for non-manifold edges and inverted normals\./i)).toBeInTheDocument();
  });

  test('renders external resource links with correct href', () => {
    render(<TroubleshootingGuide />);
    const link = screen.getByRole('link', { name: /Mesh Quality Best Practices/i });
    expect(link).toHaveAttribute('href', 'https://www.axentx.com/docs/mesh-quality');
  });

  test('renders all sections', () => {
    render(<TroubleshootingGuide />);
    const titles = ['Mesh Quality Issues', 'Convergence Failure', 'Numerical Instability (NaNs/Inf)'];
    titles.forEach(title => {
      expect(screen.getByRole('heading', { name: new RegExp(title, 'i') })).toBeInTheDocument();
    });
  });

  test('renders all steps for each section', () => {
    render(<TroubleshootingGuide />);
    guideData.forEach(item => {
      item.steps.forEach(step => {
        expect(screen.getByText(new RegExp(step, 'i'))).toBeInTheDocument();
      });
    });
  });

  test('renders all additional resources', () => {
    render(<TroubleshootingGuide />);
    guideData.forEach(item => {
      if (item.resources) {
        item.resources.forEach(resource => {
          expect(screen.getByRole('link', { name: new RegExp(resource.text, 'i') })).toHaveAttribute('href', resource.url);
        });
      }
    });
  });
});