import { performance } from 'perf_hooks';
import { v4 as uuidv4 } from 'uuid';
import { promisify } from 'util';
import { exec } from 'child_process';
import { promisify } from 'util';
import { exec } from 'child_process';

const execPromise = promisify(exec);

class PerformanceBenchmarkCollector {
  constructor() {
    this.benchmarkData = new Map();
    this.lastCollectionTime = null;
  }

  async collectSystemMetrics() {
    try {
      const metrics = {
        timestamp: new Date().toISOString(),
        systemInfo: await this.getSystemInfo(),
        cpuUsage: await this.getCpuUsage(),
        memoryUsage: await this.getMemoryUsage(),
        diskUsage: await this.getDiskUsage(),
        networkStats: await this.getNetworkStats(),
        gpuInfo: await this.getGpuInfo(),
        benchmarkResults: await this.runPerformanceTests()
      };
      
      const id = uuidv4();
      this.benchmarkData.set(id, metrics);
      this.lastCollectionTime = new Date().toISOString();
      
      return { id, metrics };
    } catch (error) {
      console.error('Error collecting performance metrics:', error);
      throw error;
    }
  }

  async getSystemInfo() {
    try {
      const { stdout } = await execPromise('uname -a');
      return stdout.trim();
    } catch (error) {
      return 'System info not available';
    }
  }

  async getCpuUsage() {
    try {
      const { stdout } = await execPromise('top -bn1 | grep "Cpu(s)" | sed "s/.*, \\(.*\\) percent.*/\\1/"');
      return parseFloat(stdout.trim());
    } catch (error) {
      return 0;
    }
  }

  async getMemoryUsage() {
    try {
      const { stdout } = await execPromise('free -m | awk '$1=="Mem:" {print $3/$2*100}'');
      return parseFloat(stdout.trim());
    } catch (error) {
      return 0;
    }
  }

  async getDiskUsage() {
    try {
      const { stdout } = await execPromise('df -h / | awk '$1=="/" {print $5}'');
      return stdout.trim();
    } catch (error) {
      return '0%';
    }
  }

  async getNetworkStats() {
    try {
      const { stdout } = await execPromise('netstat -i | grep -v lo | awk '{print $2, $3}'');
      return stdout.trim();
    } catch (error) {
      return 'Network stats not available';
    }
  }

  async getGpuInfo() {
    try {
      const { stdout } = await execPromise('nvidia-smi --query-gpu=name,utilization.gpu --format=csv,noheader');
      return stdout.trim();
    } catch (error) {
      return 'GPU info not available';
    }
  }

  async runPerformanceTests() {
    try {
      const tests = [
        {
          name: 'CPU Benchmark',
          command: 'stress --cpu 4 --timeout 1m',
          description: 'CPU stress test'
        },
        {
          name: 'Memory Benchmark',
          command: 'stress --vm 2 --timeout 1m',
          description: 'Memory stress test'
        },
        {
          name: 'Disk Benchmark',
          command: 'stress --io 1 --timeout 1m',
          description: 'Disk I/O test'
        }
      ];

      const results = [];
      for (const test of tests) {
        const start = performance.now();
        await execPromise(test.command);
        const end = performance.now();
        results.push({
          name: test.name,
          duration: (end - start) / 1000,
          description: test.description
        });
      }
      return results;
    } catch (error) {
      console.error('Error running performance tests:', error);
      return [];
    }
  }

  getLatestBenchmark() {
    if (this.benchmarkData.size === 0) {
      return null;
    }
    return Array.from(this.benchmarkData.values())[this.benchmarkData.size - 1];
  }

  getAllBenchmarks() {
    return Array.from(this.benchmarkData.values());
  }

  filterBenchmarks(filterCriteria) {
    return this.getAllBenchmarks().filter(benchmark => {
      const matchesFilter = Object.keys(filterCriteria).every(key => {
        const value = filterCriteria[key];
        if (value === undefined) return true;
        return benchmark[key] === value;
      });
      return matchesFilter;
    });
  }

  sortBenchmarks(sortBy, order = 'asc') {
    const sorted = [...this.getAllBenchmarks()];
    sorted.sort((a, b) => {
      const aValue = a[sortBy];
      const bValue = b[sortBy];
      
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return order === 'asc' ? aValue - bValue : bValue - aValue;
      }
      
      return order === 'asc' 
        ? aValue.localeCompare(bValue, 'en', { sensitivity: 'base' })
        : bValue.localeCompare(aValue, 'en', { sensitivity: 'base' });
    });
    return sorted;
  }
}

export default new PerformanceBenchmarkCollector();