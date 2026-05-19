const axios = require('axios');

const SLACK_WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL;

function notifyAssignee(assignee, task, newStatus) {
  const message = `Task ${task.title} has been updated to ${newStatus}.`;
  const payload = {
    text: message,
    username: assignee,
  };

  axios.post(SLACK_WEBHOOK_URL, payload)
    .catch((error) => {
      console.error('Error notifying assignee:', error);
    });
}

module.exports = {
  notifyAssignee,
};