const cron = require('node-cron');
const axios = require('axios');
const { updateProjectStatus, sendNotification } = require('../utils');

/**
 * Evaluates stopping criteria for all active validation projects
 */
async function evaluateStoppingCriteria() {
  try {
    const response = await axios.get('https://api.example.com/activeProjects');
    const projects = response.data;

    for (const project of projects) {
      const metricsResponse = await axios.get(`https://api.example.com/projects/${project.id}/metrics`);
      const metrics = metricsResponse.data;

      let projectStatus = 'At Risk';
      let consecutiveDaysOnTrack = 0;

      for (const metric of metrics) {
        const isBelowTarget = metric.direction === 'up'
          ? metric.value < metric.target
          : metric.value > metric.target;

        if (isBelowTarget) {
          // Metric failed threshold, project is at risk
          break;
        } else {
          // Metric met or exceeded target
          projectStatus = 'On Track';
          consecutiveDaysOnTrack++;
        }
      }

      if (consecutiveDaysOnTrack >= 3) {
        projectStatus = 'On Track';
        consecutiveDaysOnTrack = 0; // Reset counter
      } else if (projectStatus === 'On Track') {
        consecutiveDaysOnTrack = 0; // Reset counter if not at risk
      }

      await updateProjectStatus(project.id, projectStatus);

      if (projectStatus === 'At Risk') {
        await sendNotification(project.id, 'Your project is at risk. Please review your metrics.');
      } else if (projectStatus === 'On Track' && consecutiveDaysOnTrack === 3) {
        await sendNotification(project.id, 'Your project is on track after meeting targets for 3 consecutive days.');
      }
    }

    return { success: true, message: 'Stopping criteria evaluation completed' };
  } catch (error) {
    console.error('Error evaluating stopping criteria:', error);
    throw error;
  }
}

cron.schedule('0 2 * * *', evaluateStoppingCriteria);

module.exports = { evaluateStoppingCriteria };