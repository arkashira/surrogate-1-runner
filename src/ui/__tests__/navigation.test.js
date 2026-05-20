import React from 'react';
import { render, screen } from '@testing-library/react';
import Navigation from '../navigation';

test('renders navigation with framework link', () => {
  render(<Navigation />);
  expect(screen.getByText('Marketing Framework')).toBeInTheDocument();
  expect(screen.getByText('Marketing Framework')).toHaveAttribute('href', '/framework');
  expect(screen.getByText('Home')).toBeInTheDocument();
  expect(screen.getByText('Resources')).toBeInTheDocument();
});