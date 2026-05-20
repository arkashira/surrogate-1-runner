import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MarkdownModal from '../components/MarkdownModal';

test('renders markdown content in modal', () => {
  const mockMarkdownContent = '# Test Header\n\nThis is a test.';
  const mockOnRequestClose = jest.fn();

  render(<MarkdownModal isOpen={true} onRequestClose={mockOnRequestClose} markdownContent={mockMarkdownContent} />);

  expect(screen.getByText('Test Header')).toBeInTheDocument();
  expect(screen.getByText('This is a test.')).toBeInTheDocument();

  fireEvent.click(screen.getByText('Close'));
  expect(mockOnRequestClose).toHaveBeenCalled();
});