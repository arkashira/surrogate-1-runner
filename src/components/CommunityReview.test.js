import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import CommunityReview from './CommunityReview';
import { filterReviews } from '../utils/validation';

// Mock the validation module
jest.mock('../utils/validation', () => ({
  filterReviews: jest.fn(),
}));

const mockReviews = [
  { id: 1, userId: 'user1', componentId: 'comp1', rating: 5, comment: 'Excellent product!', date: '2023-01-01' },
  { id: 2, userId: 'user2', componentId: 'comp1', rating: 2, comment: 'Not good', date: '2023-01-02' },
  { id: 3, userId: 'user3', componentId: 'comp1', rating: 4, comment: 'Best ever', date: '2023-01-03' },
];

describe('CommunityReview', () => {
  beforeEach(() => {
    filterReviews.mockReturnValue(mockReviews.slice(0, 1));
  });

  test('renders loading state initially', () => {
    render(<CommunityReview componentId="comp1" />);
    expect(screen.getByText('Loading reviews...')).toBeInTheDocument();
  });

  test('renders approved reviews after loading', async () => {
    render(<CommunityReview componentId="comp1" />);
    
    await waitFor(() => {
      expect(screen.getByText('Community Reviews')).toBeInTheDocument();
      expect(screen.getByText('user1')).toBeInTheDocument();
      expect(screen.getByText('Excellent product!')).toBeInTheDocument();
    });
  });

  test('shows no reviews message when none available', async () => {
    filterReviews.mockReturnValue([]);
    render(<CommunityReview componentId="comp1" />);
    
    await waitFor(() => {
      expect(screen.getByText('No reviews available yet.')).toBeInTheDocument();
    });
  });

  test('displays error message when fetch fails', async () => {
    fetch.mockRejectOnce(new Error('Network error'));
    render(<CommunityReview componentId="comp1" />);
    
    await waitFor(() => {
      expect(screen.getByText('Error: Network error')).toBeInTheDocument();
    });
  });
});