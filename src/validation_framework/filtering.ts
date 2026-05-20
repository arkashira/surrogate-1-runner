/**
 * Filtering utilities for benchmark data.
 *
 * The benchmark data is an array of objects where each object represents a startup
 * and contains numeric metrics such as marketSize, teamExperience, funding, etc.
 *
 * The `filterBenchmarks` function allows callers to filter this array by providing
 * a set of filter criteria. Each criterion can be optional and has a minimum and maximum value.
 * Additionally, users can provide custom predicates to filter the data.
 *
 * Example usage:
 *