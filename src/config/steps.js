export const STEPS = [
  { 
    id: 'stripe', 
    title: 'Connect Stripe', 
    description: 'Link your Stripe account for payment data',
    apiCall: 'connectStripe'
  },
  { 
    id: 'ga4', 
    title: 'Connect GA4', 
    description: 'Link Google Analytics 4 for traffic data',
    apiCall: 'connectGA4'
  },
  { 
    id: 'csv', 
    title: 'Upload CSV', 
    description: 'Import your CSV export data',
    apiCall: 'uploadCSV'
  },
  { 
    id: 'review', 
    title: 'Review & Complete', 
    description: 'Verify all connections and finish setup',
    apiCall: null
  }
];