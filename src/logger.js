const { createLogger, format, transports } = require('winston');

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),          // keep stack traces
    format.splat(),
    format.json()
  ),
  transports: [
    // Console is always enabled – useful in dev & CI
    new transports.Console(),

    // In production you can add a file or external service (e.g. Loggly)
    ...(process.env.NODE_ENV === 'production'
      ? [new transports.File({ filename: '/var/log/axentx/axentx.log' })]
      : [])
  ],
});

module.exports = logger;