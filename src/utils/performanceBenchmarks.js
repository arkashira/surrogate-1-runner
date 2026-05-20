const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const DATA_FILE = path.join(__dirname, '../data/components.json');
const API_URL = 'https://api.example.com/performance-benchmarks';

class PerformanceBenchmarks {
  constructor() {
    this.benchmarks = this.loadBenchmarks();
  }

  async loadBenchmarks() {
    try {
      const data = fs.readFileSync(DATA_FILE, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      console.error('Failed to load benchmarks:', error.message);
      return this.getDefaultBenchmarks();
    }
  }

  getDefaultBenchmarks() {
    return {
      components: [
        {
          name: 'dataset-streamer',
          category: 'ingestion',
          description: 'Parallel dataset slicing and streaming worker',
          performance: {
            benchmark1: '15000 records/sec',
            benchmark2: '2.5ms avg'
          }
        },
        {
          name: 'schema-normalizer',
          category: 'processing',
          description: 'Per-schema normalization engine',
          performance: {
            benchmark1: '8000 records/sec',
            benchmark2: '5ms avg'
          }
        },
        {
          name: 'md5-deduplicator',
          category: 'processing',
          description: 'Central md5 hash store deduplication',
          performance: {
            benchmark1: '12000 records/sec',
            benchmark2: '3ms avg'
          }
        },
        {
          name: 'huggingface-uploader',
          category: 'output',
          description: 'Dataset repo upload worker',
          performance: {
            benchmark1: '5000 records/sec',
            benchmark2: '15ms avg'
          }
        }
      ]
    };
  }

  async getPerformanceBenchmarks() {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const benchmarks = await response.json();
      return benchmarks;
    } catch (error) {
      console.error('Failed to fetch performance benchmarks:', error);
      return this.getDefaultBenchmarks();
    }
  }

  getComponent(name) {
    const component = this.benchmarks.components.find(c => c.name === name);
    return component || null;
  }

  getAllComponents() {
    return this.benchmarks.components || [];
  }

  getByCategory(category) {
    return this.benchmarks.components.filter(c => c.category === category);
  }

  getPerformanceMetrics(componentName) {
    const component = this.getComponent(componentName);
    if (!component) return null;
    return {
      throughput: component.performance.benchmark1,
      latency: component.performance.benchmark2,
      memory: '256MB',
      cpu: '1 core @ 80%',
      reliability: '99.9%'
    };
  }

  compareComponents(names) {
    return names.map(name => this.getComponent(name));
  }

  saveBenchmarks(data) {
    try {
      fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
      return true;
    } catch (error) {
      console.error('Failed to save benchmarks:', error.message);
      return false;
    }
  }
}

module.exports = PerformanceBenchmarks;