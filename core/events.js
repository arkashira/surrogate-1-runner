// ... (other event handlers)

function handleAgentInteractionIssue(eventData) {
  const notifier = require('./orchestration/notifications');
  notifier.notify('agentInteractionIssue', eventData.condition);
}

module.exports = {
  // ... (other event handlers)
  handleAgentInteractionIssue,
};