class AnalyticsPipeline {
  emitEvent(eventName, eventData) {
    console.log(`Emitting event: ${eventName}`, eventData);
    // Logic to send the event data to the analytics pipeline
  }
}

module.exports = new AnalyticsPipeline();