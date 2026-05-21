import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import DataGenerationForm from '../../components/DataGenerationForm';
import { generateSyntheticData } from '../../services/dataService';

jest.mock('../../services/dataService');

describe('DataGenerationForm', () => {
  it('renders correctly', () => {
    const { getByLabelText, getByText } = render(<DataGenerationForm />);
    expect(getByLabelText('Dataset Type')).toBeInTheDocument();
    expect(getByLabelText('Number of Records')).toBeInTheDocument();
    expect(getByText('Generate Data')).toBeInTheDocument();
  });

  it('submits the form and calls generateSyntheticData', async () => {
    (generateSyntheticData as jest.Mock).mockResolvedValueOnce({});
    const { getByLabelText, getByText } = render(<DataGenerationForm />);

    fireEvent.change(getByLabelText('Dataset Type'), { target: { value: 'users' } });
    fireEvent.change(getByLabelText('Number of Records'), { target: { value: '100' } });
    fireEvent.click(getByText('Generate Data'));

    await waitFor(() => {
      expect(generateSyntheticData).toHaveBeenCalledWith({
        datasetType: 'users',
        recordCount: '100',
      });
    });
  });
});