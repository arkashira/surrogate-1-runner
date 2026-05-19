export interface Deal {
  id: string;
  name: string;
  industry: 'Tech' | 'Finance' | 'Healthcare';
  stage: 'Idea' | 'Validation' | 'Early Traction' | 'Expansion';
  location: 'US' | 'Europe' | 'Asia';
}