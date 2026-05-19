export interface InvoiceSummary {
  id: string;
  invoiceNumber: string;
  date: string;
  amount: number;
  status: string;
  recommendedAction: string;
}