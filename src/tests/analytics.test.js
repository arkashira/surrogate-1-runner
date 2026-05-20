import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import Analytics from '../ui/analytics';

describe('Analytics component', () => {
  it('renders chart with data', async () => {
    const { getByText } = render(<Analytics />);
    await waitFor(() => expect(getByText('User Engagement')).toBeInTheDocument());
  });
});