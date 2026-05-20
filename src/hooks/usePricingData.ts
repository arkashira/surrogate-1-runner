import { useQuery } from '@tanstack/react-query';
import { fetchPricingData, PricingItem } from '../api/pricing';

export const usePricingData = () =>
  useQuery<PricingItem[], Error>(['pricingData'], fetchPricingData);