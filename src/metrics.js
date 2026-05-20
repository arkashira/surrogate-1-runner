const express = require('express');
const app = express();
const fs = require('fs');

app.get('/metrics', (req, res) => {
  const costLogs = fs.readFileSync('/opt/axentx/surrogate-1/logs/cost-logs.jsonl', 'utf8');
  const logs = costLogs.split('\n').map(JSON.parse);

  const totalCost = logs.reduce((acc, log) => acc + log.cost, 0);
  const avgCost = totalCost / logs.length;
  const totalDuration = logs.reduce((acc, log) => acc + log.duration, 0);
  const avgDuration = totalDuration / logs.length;

  res.send(`cost_total ${totalCost}\ncost_avg ${avgCost}\nduration_total ${totalDuration}\nduration_avg ${avgDuration}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Metrics server listening on port ${PORT}`);
});