import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route } from 'react-router-dom';
import InstancePage from '../../src/components/InstancePage';
import { getInstanceData } from '../../src/services/api';

jest.mock('../../src/services/api');

describe('InstancePage', () => {
  it('displays the total data size', async () => {
    const mockInstanceData = {
      name: 'Test Instance',
      totalDataSize: '100 MB',
    };

    getInstanceData.mockResolvedValue(mockInstanceData);

    render(
      <MemoryRouter initialEntries={['/instances/1']}>
        <Route path="/instances/:instanceId">
          <InstancePage />
        </Route>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Total Data Size: 100 MB')).toBeInTheDocument();
    });
  });
});