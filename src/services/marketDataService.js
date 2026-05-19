
import axios from 'axios';
import csvParser from 'csv-parser';
import fs from 'fs';
import { v4 as uuidv4 } from 'uuid';
import { externalSources } from '../data/externalSources';

class MarketDataService {
  constructor() {
    this.sources = externalSources;
    this.cache = new Map();
  }

  async fetchData(sourceName) {
    const source = this.sources.find(s => s.name === sourceName);
    if (!source) {
      throw new Error(`Source "${sourceName}" not found`);
    }

    let rawData;
    
    if (source.type === 'API') {
      const response = await axios.get(source.url, {
        timeout: 10000,
        headers: source.headers || {}
      });
      rawData = response.data;
    } else if (source.type === 'CSV') {
      rawData = await this.fetchCSV(source.url);
    } else {
      throw new Error(`Unsupported source type: ${source.type}`);
    }

    return this.normalizeData(rawData, source);
  }

  async fetchCSV(url) {
    return new Promise((resolve, reject) => {
      const results = [];
      // In production, use proper streaming with axios response
      fs.createReadStream(url)
        .pipe(csvParser())
        .on('data', (data) => results.push(data))
        .on('end', () => resolve(results))
        .on('error', reject);
    });
  }

  normalizeData(rawData, source) {
    const dataArray = Array.isArray(rawData) ? rawData : [rawData];
    
    return dataArray.map(item => ({
      id: uuidv4(),
      productId: item[source.productIdField],
      price: parseFloat(item[source.priceField]),
      demand: parseFloat(item[source.demandField]),
      timestamp: new Date().toISOString(),
      source: source.name
    })).filter(item => !isNaN(item.price) && !isNaN(item.demand));
  }

  calculateElasticity(dataPoints) {
    if (dataPoints.length < 2) return null;
    
    // Sort by price to ensure proper calculation
    const sorted = [...dataPoints].sort((a, b) => a.price - b.price);
    const p1 = sorted[0].price;
    const p2 = sorted[sorted.length - 1].price;
    const q1 = sorted[0].demand;
    const q2 = sorted[sorted.length - 1].demand;

    const priceChange = (p2 - p1) / p1;
    const demandChange = (q2 - q1) / q1;

    if (priceChange === 0) return null;
    
    return {
      elasticity: demandChange / priceChange,
      priceRange: { min: p1, max: p2 },
      demandRange: { min: q1, max: q2 },
      dataPoints: sorted.length
    };
  }

  async fetchAllAndCalculate() {
    const results = [];
    
    for (const source of this.sources) {
      try {
        const data = await this.fetchData(source.name);
        
        // Group by product
        const grouped = this.groupByProduct(data);
        
        for (const [productId, points] of Object.entries(grouped)) {
          const elasticity = this.calculateElasticity(points);
          
          if (elasticity) {
            results.push({
              productId,
              source: source.name,
              ...elasticity,
              fetchedAt: new Date().toISOString()
            });
          }
        }
      } catch (error) {
        console.error(`Error fetching ${source.name}:`, error.message);
        // Continue with other sources
      }
    }

    return results;
  }

  groupByProduct(data) {
    return data.reduce((acc, item) => {
      if (!acc[item.productId]) {
        acc[item.productId] = [];
      }
      acc[item.productId].push(item);
      return acc;
    }, {});
  }

  async saveResults(data) {
    // Database implementation hook
    console.log(`Processed ${data.length} elasticity records`);
    return true;
  }
}

export default new MarketDataService();