import { renderHook } from '@testing-library/react-hooks';
import { useIntegrationStatus } from '../../hooks/useIntegrationStatus';
import { fetchIntegrationStatus } from '../../api/integration';

jest.mock('../../api/integration');

describe('useIntegrationStatus', () => {
  it('fetches integration status successfully', async () => {
    (fetchIntegrationStatus as jest.Mock).mockResolvedValue({ status: 'connected' });
    const { result, waitForNextUpdate } = renderHook(() => useIntegrationStatus());
    await waitForNextUpdate();
    expect(result.current.status).toBe('connected');
  });

  it('handles fetch error', async () => {
    (fetchIntegrationStatus as jest.Mock).mockRejectedValue(new Error('Failed to fetch'));
    const { result, waitForNextUpdate } = renderHook(() => useIntegrationStatus());
    await waitForNextUpdate();
    expect(result.current.error).toEqual(new Error('Failed to fetch'));
  });
});