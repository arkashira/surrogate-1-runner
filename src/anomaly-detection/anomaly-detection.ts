import { CloudCostData } from '../types';
import * as zscores from 'zscores';

class AnomalyDetector {
  private data: CloudCostData[] = [];
  private threshold: number;

  constructor(threshold: number) {
    this.threshold = threshold;
  }

  public addData(costData: CloudCostData): void {
    this.data.push(costData);
  }

  public detectAnomalies(): CloudCostData[] {
    const zScores = zscores.calculate(this.data.map(d => d.cost));
    return this.data.filter((_, i) => Math.abs(zScores[i]) > this.threshold);
  }
}

export default AnomalyDetector;