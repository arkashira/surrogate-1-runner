export interface Subscription {
  id: string;
  status: 'active' | 'inactive';
  current_period_end: string;
}

export interface StripeError {
  message: string;
}