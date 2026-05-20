export class SimulationResult {
  constructor(id, type, score, metrics, improvementAreas) {
    this.id = id;
    this.type = type;
    this.score = score;
    this.metrics = metrics;
    this.improvementAreas = improvementAreas;
  }

  getPerformanceLevel() {
    if (this.score >= 90) return 'excellent';
    if (this.score >= 70) return 'good';
    if (this.score >= 50) return 'fair';
    return 'poor';
  }

  getRecommendations() {
    const level = this.getPerformanceLevel();
    switch(level) {
      case 'excellent':
        return "Keep up the great work!";
      case 'good':
        return "Consider focusing on the identified areas for improvement.";
      case 'fair':
        return "This requires additional practice and review.";
      case 'poor':
        return "This scenario needs significant improvement.";
    }
  }
}