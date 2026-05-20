import java.util.logging.Logger;

public class RemediationLogger {
    private static final Logger logger = Logger.getLogger(RemediationLogger.class.getName());

    public static void logRemediation(String message) {
        logger.info(message);
    }
}