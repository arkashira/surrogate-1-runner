import java.util.logging.Logger;

public class RemediationAudit {
    private static final Logger logger = Logger.getLogger(RemediationAudit.class.getName());

    public static void auditRemediation(String message) {
        logger.info(message);
    }
}