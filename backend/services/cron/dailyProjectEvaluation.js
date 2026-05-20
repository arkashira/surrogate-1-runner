const { Project, Metric } = require('../models');
const notificationService = require('../services/notification');

async function evaluateProjects() {
  const activeProjects = await Project.findAll({ where: { status: 'active' } });
  
  for (const project of activeProjects) {
    const metrics = await Metric.findAll({ where: { projectId: project.id } });
    const latestMetrics = metrics.map(m => ({
      name: m.name,
      value: m.latestValue,
      target: m.target,
      passed: m.latestValue >= m.target
    }));

    const allPassed = latestMetrics.every(m => m.passed);
    const failedMetrics = latestMetrics.filter(m => !m.passed);

    if (failedMetrics.length > 0) {
      await handleAtRiskProject(project, latestMetrics);
    } else {
      await handleOnTrackProject(project, latestMetrics);
    }
  }
}

async function handleAtRiskProject(project, metrics) {
  await project.update({ status: 'At Risk' });
  
  await notificationService.sendProjectStatusNotification(
    project,
    'At Risk',
    metrics,
    null
  );
}

async function handleOnTrackProject(project, metrics) {
  const consecutiveDays = await getConsecutiveDaysOnTrack(project.id);
  
  if (consecutiveDays >= 3) {
    await project.update({ status: 'On Track' });
    
    await notificationService.sendProjectStatusNotification(
      project,
      'On Track',
      metrics,
      consecutiveDays
    );
  }
}

async function getConsecutiveDaysOnTrack(projectId) {
  // Implementation to check consecutive days on track
  // This would query the evaluation history for the project
  // Placeholder implementation
  return 3; // For demo purposes
}

module.exports = { evaluateProjects };