const monitoring = require('./monitoring');
const config = require('./config');

setInterval(async () => {
  const health = await monitoring.checkParserHealth();
  console.log('Parser Health:', health);
}, config.monitoringInterval);