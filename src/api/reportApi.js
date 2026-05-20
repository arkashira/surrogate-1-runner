import axios from 'axios';
import { toast } from 'react-toastify';

export async function generateInvestorReport(tenantId) {
  try {
    const response = await axios.get(`/reports/${tenantId}/latest.pdf`, {
      responseType: 'blob',
    });
    const url = URL.createObjectURL(response.data);
    const a = document.createElement('a');
    a.href = url;
    a.download = `investor-report-${tenantId}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    toast.error('Failed to generate investor report. Please try again.');
  }
}