import axios from 'axios';
import { fetchIntegrationStatus } from '../../api/integration';

jest.mock('axios');

describe('fetchIntegrationStatus', () => {
  it('fetches integration status successfully', async () => {
    (axios.get as jest.Mock).mockResolvedValue({ data: { status: 'connected' } });
    const status = await fetchIntegrationStatus();
    expect(status).toEqual({ status: 'connected' });
  });

  it('handles fetch error', async () => {
    (axios.get as jest.Mock).mockRejectedValue(new Error('Failed to fetch'));
    await expect(fetchIntegrationStatus()).rejects.toThrow('Failed to fetch integration status');
  });
});