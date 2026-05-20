import { FeedbackSystem } from './feedback.js';
import { SimulationResult } from './simulation-result.js';

export class FeedbackController {
  constructor() {
    this.feedbackSystem = new FeedbackSystem();
  }

  processSimulationResult(result) {
    const feedback = this.feedbackSystem.saveFeedback(result, result.user);
    return {
      feedback: feedback,
      history: this.feedbackSystem.getPerformanceHistory(result.user)
    };
  }

  getFeedbackHistory(user) {
    return this.feedbackSystem.getPerformanceHistory(user);
  }

  getFeedbackForSimulation(simId) {
    // In a real system, this would query the database
    return {
      id: simId,
      feedback: "This is a sample feedback for simulation",
      score: 85,
      timestamp: new Date().toISOString()
    };
  }
}