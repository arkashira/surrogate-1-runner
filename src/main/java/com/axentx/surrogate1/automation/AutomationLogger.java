import java.util.logging.Logger;
import java.util.logging.Level;

public class AutomationLogger {
    private static final Logger logger = Logger.getLogger(AutomationLogger.class.getName());

    public static void logAction(String action) {
        logger.log(Level.INFO, "Action: " + action);
    }

    public static void logResult(String result) {
        logger.log(Level.INFO, "Result: " + result);
    }
}