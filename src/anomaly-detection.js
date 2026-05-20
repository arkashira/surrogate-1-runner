class CostAnomalyDetector extends EventEmitter {
  constructor(options = {}) {
    super();
    // Threshold configuration with sensible defaults
    this.thresholds = {
      spikePercentage: options.spikePercentage || 50,
      dailyBudgetMultiplier: options.dailyBudgetMultiplier || 1.2,
      weeklyTrendThreshold: options.weeklyTrendThreshold || 0.3,
      minDataPoints: options.minDataPoints || 5,
      detectionWindowMs: options.detectionWindowMs || 60000
    };
    
    // User preference management
    this.userPreferences = new Map();
    
    // Data storage with automatic cleanup
    this.costHistory = [];
    this.anomalyHistory = [];
    
    // Alert cooldown mechanism
    this.alertCooldownMs = options.alertCooldownMs || 300000;
    this.lastAlertTime = new Map();
  }
}