import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { parseInvoice } from '../utils/invoiceParser';
import '../styles/InvoiceUpload.css';

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

const InvoiceUpload: React.FC = () => {
  const [invoiceData, setInvoiceData] = useState<InvoiceData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    setIsLoading(true);
    setError(null);

    try {
      const file = acceptedFiles[0];
      const data = await parseInvoice(file);
      setInvoiceData(data);
    } catch (err) {
      setError('Failed to parse invoice. Please try another file.');
      console.error('Invoice parsing error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxFiles: 1
  });

  return (
    <div className="invoice-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the invoice here...</p>
        ) : (
          <p>Drag and drop an invoice here, or click to select one</p>
        )}
      </div>

      {isLoading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Processing invoice...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {invoiceData && (
        <div className="invoice-preview">
          <h2>Invoice Breakdown</h2>
          <div className="invoice-sections">
            <div className="line-items">
              <h3>Line Items</h3>
              <ul>
                {invoiceData.lineItems.map((item, index) => (
                  <li key={index}>
                    <span>{item.description}</span>
                    <span>${item.amount.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="totals">
              <h3>Totals</h3>
              <p>Subtotal: ${invoiceData.subtotal.toFixed(2)}</p>
              <p>Tax: ${invoiceData.tax.toFixed(2)}</p>
              <p className="total-amount">Total: ${invoiceData.total.toFixed(2)}</p>
            </div>
          </div>

          {invoiceData.explanations && (
            <div className="explanations">
              <h3>Explanations</h3>
              <p>{invoiceData.explanations}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default InvoiceUpload;