class Logger {
  static info(message, data = {}) {
    const logEntry = {
      level: 'INFO',
      message: message,
      data: data,
      timestamp: new Date().toISOString()
    };
    
    console.log(JSON.stringify(logEntry));
  }

  static warn(message, data = {}) {
    const logEntry = {
      level: 'WARN',
      message: message,
      data: data,
      timestamp: new Date().toISOString()
    };
    
    console.warn(JSON.stringify(logEntry));
  }

  static error(message, data = {}) {
    const logEntry = {
      level: 'ERROR',
      message: message,
      data: data,
      timestamp: new Date().toISOString()
    };
    
    console.error(JSON.stringify(logEntry));
  }

  static debug(message, data = {}) {
    const logEntry = {
      level: 'DEBUG',
      message: message,
      data: data,
      timestamp: new Date().toISOString()
    };
    
    console.debug(JSON.stringify(logEntry));
  }
}

module.exports = Logger;