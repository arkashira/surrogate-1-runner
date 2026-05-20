export type StartupStage = 'seed' | 'series_a' | 'series_b' | 'growth';

export interface ComparableStartup {
  id: string;
  name: string;
  marketSize: number;          // millions USD
  teamExperience: number;      // average years
  stage: StartupStage;
  founded: string;             // ISO date
  location: string;
}

/**
 * In‑memory mock data – replace with DB queries in production.
 */
export const comparableStartups: ComparableStartup[] = [
  {
    id: '1',
    name: 'AlphaTech',
    marketSize: 1200,
    teamExperience: 8,
    stage: 'series_a',
    founded: '2018-04-12',
    location: 'San Francisco',
  },
  {
    id: '2',
    name: 'BetaHealth',
    marketSize: 850,
    teamExperience: 5,
    stage: 'seed',
    founded: '2019-09-30',
    location: 'Boston',
  },
  {
    id: '3',
    name: 'GammaFinance',
    marketSize: 2000,
    teamExperience: 12,
    stage: 'series_b',
    founded: '2016-01-20',
    location: 'New York',
  },
  {
    id: '4',
    name: 'DeltaEdu',
    marketSize: 400,
    teamExperience: 3,
    stage: 'seed',
    founded: '2020-07-15',
    location: 'Austin',
  },
  {
    id: '5',
    name: 'EpsilonEats',
    marketSize: 950,
    teamExperience: 6,
    stage: 'series_a',
    founded: '2017-11-05',
    location: 'Seattle',
  },
];