export const formatCurrency = (value: number, currency = 'USD'): string => 
  new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);

export const formatPercentage = (value: number): string => 
  `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;

export const formatDate = (date: string, options?: Intl.DateTimeFormatOptions): string => 
  new Date(date).toLocaleDateString('en-US', options || { month: 'short', day: 'numeric' });

export const formatNumber = (value: number): string => 
  new Intl.NumberFormat('en-US').format(value);