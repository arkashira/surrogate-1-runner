import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import FeedbackForm from './FeedbackForm';

jest.mock('axios');

describe('FeedbackForm', () => {
  it('submits feedback successfully', async () => {
    axios.post.mockResolvedValueOnce({ status: 200 });

    const { getByLabelText, getByText } = render(<FeedbackForm />);

    fireEvent.change(getByLabelText('Name'), { target: { value: 'John Doe' } });
    fireEvent.change(getByLabelText('Email'), { target: { value: 'john.doe@example.com' } });
    fireEvent.change(getByLabelText('Feedback'), { target: { value: 'Great troubleshooting guide!' } });

    fireEvent.click(getByText('Submit'));

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith('/api/feedback', {
        name: 'John Doe',
        email: 'john.doe@example.com',
        feedback: 'Great troubleshooting guide!',
      });
      expect(getByText('Thank you for your feedback!')).toBeInTheDocument();
    });
  });

  it('shows validation errors', async () => {
    const { getByLabelText, getByText, queryByText } = render(<FeedbackForm />);

    fireEvent.click(getByText('Submit'));

    await waitFor(() => {
      expect(getByText('Name is required')).toBeInTheDocument();
      expect(getByText('Email is required')).toBeInTheDocument();
      expect(getByText('Feedback is required')).toBeInTheDocument();
      expect(queryByText('Thank you for your feedback!')).not.toBeInTheDocument();
    });
  });
});