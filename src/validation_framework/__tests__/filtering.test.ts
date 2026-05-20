import { filterBenchmarks, Benchmark } from '../filtering';

describe('filterBenchmarks', () => {
  const sampleData: Benchmark[] = [
    { id: 1, marketSize: 500_000, teamExperience: 3, funding: 1_000_000 },
    { id: 2, marketSize: 2_000_000, teamExperience: 5, funding: 5_000_000 },
    { id: 3, marketSize: 1_500_000, teamExperience: 2, funding: 2_000_000 },
  ];

  it('returns all items when no criteria are provided', () => {
    const result = filterBenchmarks(sampleData, {});
    expect(result).toHaveLength(3);
  });

  it('filters by a single metric', () => {
    const result = filterBenchmarks(sampleData, { marketSize: { min: 1_000_000 } });
    expect(result).toHaveLength(2);
    expect(result.map((b) => b.id)).toEqual([2, 3]);
  });

  it('filters by multiple metrics', () => {
    const result = filterBenchmarks(sampleData, {
      marketSize: { min: 1_000_000 },
      teamExperience: { min: 4 },
    });
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe(2);
  });

  it('applies custom predicates (AND logic)', () => {
    const result = filterBenchmarks(sampleData, {
      marketSize: { min: 1_000_000 },
      teamExperience: { min: 4 },
      customPredicate: (b) => b.funding <= 2_000_000,
    });
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe(3);
  });

  it('throws if data is not an array', () => {
    // @ts-ignore
    expect(() => filterBenchmarks(null, {})).toThrow(TypeError);
  });
});