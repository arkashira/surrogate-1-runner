import fs from 'fs';
import path from 'path';
import axios from 'axios';

export type Benchmark = {
  id: string;
  size: string;
  domain: string;
  cost_per_month?: number;          // from local file
  cost_patterns?: string[];         // from API
  description?: string;
};

export type Filter = {
  size?: string;
  domain?: string;
  live?: boolean;   // true → fetch from API, false → use local cache
};

export class BenchmarkService {
  private static instance: BenchmarkService;
  private cache: Benchmark[] | null = null;
  private readonly dataPath = path.resolve(
    __dirname,
    '../../data/BenchmarkData.json'
  );
  private readonly apiBase = 'https://api.industry-benchmarks.com';

  private constructor() {}

  static getInstance(): BenchmarkService {
    if (!BenchmarkService.instance) {
      BenchmarkService.instance = new BenchmarkService();
    }
    return BenchmarkService.instance;
  }

  /** Load the JSON file once and cache it */
  private loadLocalData(): Benchmark[] {
    if (this.cache) return this.cache;
    try {
      const raw = fs.readFileSync(this.dataPath, 'utf8');
      this.cache = JSON.parse(raw);
    } catch (err) {
      console.error('BenchmarkService: failed to load local data', err);
      this.cache = [];
    }
    return this.cache;
  }

  /** Fetch from the remote API */
  private async fetchRemote(filter: Filter): Promise<Benchmark[]> {
    try {
      const resp = await axios.get<Benchmark[]>(`${this.apiBase}/benchmarks`, {
        params: filter,
      });
      return resp.data;
    } catch (err) {
      console.warn('BenchmarkService: remote fetch failed, falling back to local', err);
      return this.loadLocalData();
    }
  }

  /** Public entry point */
  async getBenchmarks(filter: Filter = {}): Promise<Benchmark[]> {
    const { live = false, size, domain } = filter;

    const data = live
      ? await this.fetchRemote(filter)
      : this.loadLocalData();

    return data.filter((b) => {
      const sizeMatch = size ? b.size === size : true;
      const domainMatch = domain ? b.domain === domain : true;
      return sizeMatch && domainMatch;
    });
  }

  /** Helpers for UI dropdowns */
  getAllSizes(): string[] {
    return [...new Set(this.loadLocalData().map((b) => b.size))];
  }

  getAllDomains(): string[] {
    return [...new Set(this.loadLocalData().map((b) => b.domain))];
  }
}