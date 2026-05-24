const { exec } = require('child_process');

function detectXmlParser() {
  return new Promise((resolve, reject) => {
    exec('ps aux | grep -i "xmlparser"', (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        const parserProcesses = stdout.split('\n').filter(line => line.includes('xmlparser'));
        resolve(parserProcesses.length > 0);
      }
    });
  });
}

module.exports = detectXmlParser;