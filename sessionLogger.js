const fs = require('fs');
const path = require('path');
const { createWriteStream } = require('fs');

const logDir = '/opt/axentx/surrogate-1/logs/terminal';

if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
}

function logSession(sessionData) {
    const logFilePath = path.join(logDir, `${Date.now()}.log`);
    const logStream = createWriteStream(logFilePath);

    logStream.write(JSON.stringify(sessionData));
    logStream.end();

    setTimeout(() => {
        fs.readdir(logDir, (err, files) => {
            if (err) throw err;

            files.forEach(file => {
                const filePath = path.join(logDir, file);
                const stats = fs.statSync(filePath);

                if (Date.now() - stats.mtimeMs > 90 * 24 * 60 * 60 * 1000) {
                    fs.unlinkSync(filePath);
                }
            });
        });
    }, 0);
}

module.exports = { logSession };