import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SettingsView from '../views/SettingsView';

describe('SettingsView', () => {
  it('should render correctly', () => {
    render(<SettingsView onSave={() => {}} />);
    expect(screen.getByText('CodeMuse Settings')).toBeInTheDocument();
  });

  it('should save settings', async () => {
    const onSaveMock = jest.fn();
    render(<SettingsView onSave={onSaveMock} />);

    fireEvent.change(screen.getByLabelText(/Endpoint URL/), { target: { value: 'http://example.com' } });
    fireEvent.change(screen.getByLabelText(/Suggestion Depth/), { target: { value: 'medium' } });
    fireEvent.click(screen.getByText('Save Settings'));

    expect(onSaveMock).toHaveBeenCalledWith({ endpointUrl: 'http://example.com', suggestionDepth: 'medium' });
  });
});