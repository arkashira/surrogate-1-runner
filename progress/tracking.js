class ProgressTracker {
  constructor() {
    this.progress = {};
  }

  trackProgress(language, topic, score) {
    if (!this.progress[language]) {
      this.progress[language] = {};
    }
    this.progress[language][topic] = score;
  }

  getProgress(language) {
    return this.progress[language];
  }

  getAllProgress() {
    return this.progress;
  }

  visualizeProgress(language) {
    const progress = this.getProgress(language);
    const topics = Object.keys(progress);
    const scores = topics.map(topic => progress[topic]);
    const averageScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    return {
      topics,
      scores,
      averageScore
    };
  }
}

module.exports = ProgressTracker;