import java.util.logging.Logger;

public class AutomationRunner {
    private final AutomationLogger logger;
    private final AutomationTrigger trigger;

    public AutomationRunner(AutomationLogger logger, AutomationTrigger trigger) {
        this.logger = logger;
        this.trigger = trigger;
    }

    public void run() {
        // Run automation script implementation
        logger.logAction("Running automation script");
        trigger.triggerScheduled();
        logger.logResult("Automation script completed successfully");
    }
}