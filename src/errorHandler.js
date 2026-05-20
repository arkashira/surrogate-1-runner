class ErrorHandler {
  static handleParseError(error, filePath, lineNumber) {
    const errorInfo = {
      type: 'PARSE_ERROR',
      message: error.message,
      filePath: filePath,
      lineNumber: lineNumber,
      timestamp: new Date().toISOString()
    };

    // Log the error
    console.error(`[PARSE ERROR] ${filePath}:${lineNumber} - ${error.message}`);

    // Return structured error for further processing
    return errorInfo;
  }

  static handleFileReadError(error, filePath) {
    const errorInfo = {
      type: 'FILE_READ_ERROR',
      message: error.message,
      filePath: filePath,
      timestamp: new Date().toISOString()
    };

    console.error(`[FILE READ ERROR] ${filePath} - ${error.message}`);
    return errorInfo;
  }

  static handleDependencyError(error, dependencyName, filePath) {
    const errorInfo = {
      type: 'DEPENDENCY_ERROR',
      message: error.message,
      dependencyName: dependencyName,
      filePath: filePath,
      timestamp: new Date().toISOString()
    };

    console.error(`[DEPENDENCY ERROR] ${dependencyName} in ${filePath} - ${error.message}`);
    return errorInfo;
  }
}

module.exports = ErrorHandler;