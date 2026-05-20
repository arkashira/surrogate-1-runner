import { BenchmarkService, Benchmark, Filter } from './benchmarkService';

export class DataService {
  private readonly benchmarkService = BenchmarkService.getInstance();

  async getBenchmarks(filter: Filter): Promise<Benchmark[]> {
    return this.benchmarkService.getBenchmarks(filter);
  }

  getSizes() {
    return this.benchmarkService.getAllSizes();
  }

  getDomains() {
    return this.benchmarkService.getAllDomains();
  }
}