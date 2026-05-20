import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class AutomationScheduler {
    public static void main(String[] args) {
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        AutomationTrigger trigger = new AutomationTrigger(scheduler);
        AutomationLogger logger = new AutomationLogger();
        AutomationRunner runner = new AutomationRunner(logger, trigger);
        runner.run();
    }
}