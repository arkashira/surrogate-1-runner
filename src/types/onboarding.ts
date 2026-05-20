export type ProductType =
  | 'saas'
  | 'marketplace'
  | 'ecommerce'
  | 'content'
  | 'fintech'
  | 'healthtech'
  | 'edtech'
  | 'other';

export type MarketingChannel =
  | 'seo'
  | 'paid_ads'
  | 'social'
  | 'email'
  | 'content'
  | 'referral'
  | 'partnerships'
  | 'community'
  | 'none';

export interface OnboardingFormData {
  // Account
  email: string;
  password: string;
  authMethod: 'email' | 'oauth';

  // Product
  productType: ProductType;
  productName: string;
  productDescription?: string;

  // Metrics
  mrr: string; // keep as string for easy input handling, convert on submit
  mau: string;
  launchDate: string; // ISO date (yyyy-mm-dd)

  // Marketing
  marketingChannels: MarketingChannel[];
  monthlyMarketingBudget?: string;
}