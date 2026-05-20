const { createLogger, transports, format } = require('winston');
const { combine, timestamp, label, prettyPrint } = format;

const logger = createLogger({
  format: combine(
    label({ label: 'terminal-server' }),
    timestamp(),
    prettyPrint()
  ),
  transports: [
    new transports.File({ filename: '/opt/axentx/surrogate-1/logs/terminal/info.log', level: 'info' }),
    new transports.File({ filename: '/opt/axentx/surrogate-1/logs/terminal/error.log', level: 'error' })
  ],
  exceptionHandlers: [
    new transports.File({ filename: '/opt/axentx/surrogate-1/logs/terminal/exceptions.log' })
  ]
});

module.exports = logger;