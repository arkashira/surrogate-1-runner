import axios from 'axios';
import { toast } from 'react-toastify';
import { generateInvestorReport } from './reportApi';

jest.mock('axios');
jest.mock('react-toastify');

describe('generateInvestorReport', () => {
  it('sends GET request to /reports/{tenantId}/latest.pdf', async () => {
    const tenantId = 'your-tenant-id'; // replace with actual tenant ID
    await generateInvestorReport(tenantId);
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith(`/reports/${tenantId}/latest.pdf`, {
      responseType: 'blob',
    });
  });

  it('displays toast notification on error', async () => {
    const tenantId = 'your-tenant-id'; // replace with actual tenant ID
    const error = new Error('Test error');
    axios.get.mockRejectedValue(error);
    await generateInvestorReport(tenantId);
    expect(toast.error).toHaveBeenCalledTimes(1);
    expect(toast.error).toHaveBeenCalledWith('Failed to generate investor report. Please try again.');
  });
});