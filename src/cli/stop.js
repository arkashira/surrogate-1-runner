const fs = require('fs');
const pid = fs.readFileSync('surrogate-1.pid', 'utf8');
process.kill(pid, 'SIGTERM');
fs.unlinkSync('surrogate-1.pid');
console.log('Sandbox stopped');