import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.logging.Logger;

@Component
public class InsightEmailWorker {

    private final Logger logger = Logger.getLogger(InsightEmailWorker.class.getName());

    @Scheduled(fixedDelay = 86400000) // 86400000 milliseconds = 1 day
    public void sendInsightEmails() {
        // Get users with linked accounts
        // ...

        // Filter users with no linked accounts
        // ...

        // Send email to users with linked accounts
        // ...
    }
}