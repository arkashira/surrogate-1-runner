export const fetchComponentBenchmarks = async (componentId) => {
  try {
    const response = await fetch(`/api/components/${componentId}/benchmarks`);
    if (!response.ok) throw new Error('Benchmark data fetch failed');
    return await response.json();
  } catch (error) {
    console.error('Benchmark API error:', error);
    throw error;
  }
};