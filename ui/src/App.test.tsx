import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders troubleshooting guide', () => {
  render(<App />);
  const linkElement = screen.getByText(/Troubleshooting Guide/i);
  expect(linkElement).toBeInTheDocument();
});

test('renders search input', () => {
  render(<App />);
  const searchInput = screen.getByPlaceholderText(/Search the guide.../i);
  expect(searchInput).toBeInTheDocument();
});

test('renders guide content', () => {
  render(<App />);
  const guideContent = screen.getByText(/Common Issues/i);
  expect(guideContent).toBeInTheDocument();
});