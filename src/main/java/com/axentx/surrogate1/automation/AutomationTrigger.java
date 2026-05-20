import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class AutomationTrigger {
    private final ScheduledExecutorService scheduler;

    public AutomationTrigger(ScheduledExecutorService scheduler) {
        this.scheduler = scheduler;
    }

    public void triggerManual() {
        // Manual trigger implementation
    }

    public void triggerScheduled() {
        // Scheduled trigger implementation
    }
}