import { render, screen, fireEvent } from '@testing-library/react';
import CloudSettings from '../settings';

test('cloud provider switching functionality', async () => {
  render(<CloudSettings />);
  
  // Verify initial state
  expect(screen.getByText('Amazon Web Services')).toBeSelected();
  expect(screen.getByRole('button', { name: /import cost data/i })).toBeEnabled();
  
  // Switch to GCP
  const providerSelect = screen.getByRole('combobox');
  fireEvent.change(providerSelect, { target: { value: 'gcp' } });
  expect(screen.getByText('Google Cloud Platform')).toBeSelected();
  
  // Trigger import
  fireEvent.click(screen.getByRole('button', { name: /import cost data/i }));
  expect(screen.getByText(/importing.../i)).toBeInTheDocument();
});