import { SimulationResult } from './simulation-result.js';

class FeedbackSystem {
  constructor() {
    this.feedbackTemplates = {
      basic: {
        success: "Great job! You've successfully completed the simulation.",
        improvement: "You're getting closer. Try focusing on {area} next time.",
        critical: "Need more practice here. Let's review the key points."
      },
      professional: {
        success: "Excellent performance! Your approach was professional and effective.",
        improvement: "Consider adjusting your approach in {area} for better outcomes.",
        critical: "This requires immediate attention. Review the professional guidelines."
      },
      technical: {
        success: "Perfect technical execution! Your skills are impressive.",
        improvement: "Check {area} for potential improvements in your methodology.",
        critical: "This requires immediate technical review and correction."
      }
    };
  }

  generateFeedback(result) {
    const template = this.feedbackTemplates[result.type] || this.feedbackTemplates.basic;
    const feedback = {
      overall: template.success,
      detailed: [],
      performanceScore: result.score,
      areasForImprovement: result.improvementAreas,
      timestamp: new Date().toISOString()
    };

    if (result.score < 70) {
      feedback.overall = template.critical;
      feedback.detailed.push("Your performance needs significant improvement.");
    } else if (result.score < 90) {
      feedback.overall = template.improvement;
      feedback.detailed.push(`Focus on ${result.improvementAreas.join(', ')}`);
    }

    return feedback;
  }

  saveFeedback(result, user) {
    const feedback = this.generateFeedback(result);
    const feedbackData = {
      user: user,
      simulationId: result.id,
      timestamp: feedback.timestamp,
      score: feedback.performanceScore,
      feedback: feedback.overall,
      detailedFeedback: feedback.detailed,
      improvementAreas: feedback.areasForImprovement,
      performanceMetrics: result.metrics
    };

    // In a real system, this would persist to a database
    console.log("Saving feedback:", feedbackData);
    return feedbackData;
  }

  getPerformanceHistory(user) {
    // In a real system, this would query a database
    return [
      { date: '2024-05-10', score: 85, scenario: 'Client Meeting' },
      { date: '2024-05-09', score: 72, scenario: 'Technical Presentation' },
      { date: '2024-05-08', score: 90, scenario: 'Project Review' }
    ];
  }
}

// Export the class for use in other modules
export { FeedbackSystem };