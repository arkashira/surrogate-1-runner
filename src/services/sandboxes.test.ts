import axios from 'axios';
import { deleteSandbox } from './sandboxes';

jest.mock('axios');

describe('deleteSandbox', () => {
  const mockedAxios = axios as jest.Mocked<typeof axios>;
  const sandboxId = 'test-sandbox-123';

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should successfully delete a sandbox', async () => {
    mockedAxios.delete.mockResolvedValueOnce({ status: 204 });

    await expect(deleteSandbox(sandboxId)).resolves.not.toThrow();
    expect(mockedAxios.delete).toHaveBeenCalledWith(
      expect.stringContaining(`/sandboxes/${sandboxId}`)
    );
  });

  it('should throw error when sandbox not found', async () => {
    mockedAxios.delete.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 404 }
    });

    await expect(deleteSandbox(sandboxId)).rejects.toThrow('not found');
  });

  it('should throw error on API failure', async () => {
    mockedAxios.delete.mockRejectedValueOnce({
      isAxiosError: true,
      message: 'Network error'
    });

    await expect(deleteSandbox(sandboxId)).rejects.toThrow();
  });
});