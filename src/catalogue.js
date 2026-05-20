/**
 * Build catalogue.
 *
 * In production replace the export with a DB call (e.g. async function loadCatalogue())
 * but keep the same shape: [{ id, name, price, tags }]
 */
const BUILD_CATALOGUE = [
  {
    id: 'build-001',
    name: 'Entry‑Level Gaming',
    price: 800,
    tags: ['gaming', 'budget'],
  },
  {
    id: 'build-002',
    name: 'Mid‑Range Gaming',
    price: 1300,
    tags: ['gaming', 'streaming'],
  },
  {
    id: 'build-003',
    name: 'Content Creation',
    price: 1800,
    tags: ['video editing', 'rendering', 'streaming'],
  },
  {
    id: 'build-004',
    name: 'Professional Workstation',
    price: 2500,
    tags: ['video editing', '3d modeling', 'rendering'],
  },
  {
    id: 'build-005',
    name: 'Ultra‑High‑End Gaming',
    price: 3000,
    tags: ['gaming', 'ray tracing', 'high fps'],
  },
  {
    id: 'build-006',
    name: 'Budget Office',
    price: 600,
    tags: ['office', 'budget'],
  },
];

module.exports = { BUILD_CATALOGUE };