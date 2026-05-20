export interface OptimizationSuggestion {
  id: string;
  title: string;
  description: string;
  action: string;
  acknowledged?: boolean; // added by API
}