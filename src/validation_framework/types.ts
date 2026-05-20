export interface StartupBenchmark {
  id: string;
  name: string;
  marketSize: number;      // millions USD
  teamExperience: number;  // average years
  funding: number;         // millions USD
  stage: string;           // e.g. "Seed", "Series A"
  metrics?: Record<string, number>; // optional extra metrics
}

export interface BenchmarkFilters {
  minMarketSize?: number;
  maxMarketSize?: number;
  minTeamExperience?: number;
  maxTeamExperience?: number;
  stage?: string;
}