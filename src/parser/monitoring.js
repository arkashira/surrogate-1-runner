const { promisify } = require('util');
const exec = promisify(require('child_process').exec);

async function checkParserHealth() {
  try {
    const { stdout } = await exec('cat /opt/axentx/surrogate-1/logs/parser.log | grep "error" | wc -l');
    const errorCount = parseInt(stdout.trim(), 10);
    return { healthy: errorCount === 0, errorCount };
  } catch (error) {
    console.error('Error checking parser health:', error);
    return { healthy: false, errorCount: null };
  }
}

module.exports = {
  checkParserHealth,
};