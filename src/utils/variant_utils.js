export const getVariants = () => [
  {
    id: 1,
    name: 'Variant A',
    openaiCompatibility: true,
    containerizationSupport: true,
    integrationPatterns: ['API', 'SDK'],
  },
  {
    id: 2,
    name: 'Variant B',
    openaiCompatibility: false,
    containerizationSupport: true,
    integrationPatterns: ['CLI'],
  },
  // Add more variants as needed
];

export const getVariantColumns = () => {
  return [
    { label: 'OpenAI Compatibility', key: 'openaiCompatibility' },
    { label: 'Containerization Support', key: 'containerizationSupport' },
    { label: 'Integration Patterns', key: 'integrationPatterns' },
  ];
};

export const compareVariants = (selectedVariants) => {
  // Logic to compare selected variants and return comparison data
  // ...
};