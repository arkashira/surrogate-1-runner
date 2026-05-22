import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class InsightEmailService {

    private final InsightEmailWorker insightEmailWorker;

    @Autowired
    public InsightEmailService(InsightEmailWorker insightEmailWorker) {
        this.insightEmailWorker = insightEmailWorker;
    }

    public void sendInsightEmails() {
        insightEmailWorker.sendInsightEmails();
    }
}