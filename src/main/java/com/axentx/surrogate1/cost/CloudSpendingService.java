import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CloudSpendingService {

    private final AnomalyDetector anomalyDetector;
    private final AlertService alertService;
    private final List<Double> historicalValues = // Fetch historical values from the database or other storage

    public CloudSpendingService(AnomalyDetector anomalyDetector, AlertService alertService) {
        this.anomalyDetector = anomalyDetector;
        this.alertService = alertService;
    }

    @Scheduled(fixedDelay = 60000) // Check every minute
    public void checkForAnomalies() {
        double currentSpending = // Fetch current spending from the cloud provider API

        if (anomalyDetector.isAnomaly(currentSpending, historicalValues)) {
            String subject = "Cloud Spending Alert: Unexpected Spike Detected";
            String text = "Anomaly detected in cloud spending. Current spending: " + currentSpending + "\nSuggested action: Investigate and mitigate budget overruns.";
            alertService.sendEmailAlert("finance@example.com", subject, text);
        }
    }
}