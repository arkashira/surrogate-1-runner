export interface UpgradeRecommendation {
  componentNames: string[];
  price: number;
  expectedFPS: number;
  roi: number;
}