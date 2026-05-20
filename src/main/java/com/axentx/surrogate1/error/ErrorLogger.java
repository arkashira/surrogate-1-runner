import java.util.logging.Logger;

public class ErrorLogger {
    private static final Logger logger = Logger.getLogger(ErrorLogger.class.getName());
    private ErrorLog errorLog;

    public void logError(String errorMessage) {
        // Log error
        logger.severe(errorMessage);
        errorLog = new ErrorLog(errorMessage);
    }

    public ErrorLog getErrorLog() {
        return errorLog;
    }
}