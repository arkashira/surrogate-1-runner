import axios from 'axios';

interface InvoiceItem {
  description: string;
  amount: number;
}

interface InvoiceData {
  lineItems: InvoiceItem[];
  subtotal: number;
  tax: number;
  total: number;
  explanations?: string;
}

export const parseInvoice = async (file: File): Promise<InvoiceData> => {
  // In a real implementation, you would:
  // 1. Upload the file to your backend service
  // 2. Process it with an OCR service or invoice parsing API
  // 3. Return the structured data

  // For this example, we'll simulate an API call
  try {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // In a real app, you would replace this with actual API call:
    // const response = await axios.post('/api/parse-invoice', formData);
    // return response.data;

    // Mock data for demonstration
    return {
      lineItems: [
        { description: 'Product A', amount: 10.99 },
        { description: 'Product B', amount: 20.50 },
        { description: 'Service C', amount: 15.75 }
      ],
      subtotal: 47.24,
      tax: 4.72,
      total: 51.96,
      explanations: 'This invoice includes all items purchased and services rendered.'
    };
  } catch (error) {
    console.error('Error parsing invoice:', error);
    throw new Error('Failed to parse invoice');
  }
};