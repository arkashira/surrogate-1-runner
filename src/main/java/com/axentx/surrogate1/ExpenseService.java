import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;

import static com.axentx.surrogate1.utils.DataUtils.getHistoricalExpenses;
import static com.axentx.surrogate1.utils.DataUtils.getRecentExpenses;

@Service
public class ExpenseService {
    private final AnomalyDetector anomalyDetector;
    private final ExpenseAlertService expenseAlertService;

    public ExpenseService(AnomalyDetector anomalyDetector, ExpenseAlertService expenseAlertService) {
        this.anomalyDetector = anomalyDetector;
        this.expenseAlertService = expenseAlertService;
    }

    @Scheduled(fixedDelay = 300000) // 5 minutes
    public void checkForAnomalies() {
        List<Double> recentExpenses = getRecentExpenses();
        List<Double> historicalMean = getHistoricalExpenses().stream().mapToDouble(expense -> expense.getMean()).toList();
        List<Double> historicalStdDev = getHistoricalExpenses().stream().mapToDouble(expense -> expense.getStdDev()).toList();

        if (anomalyDetector.isAnomaly(recentExpenses, historicalMean, historicalStdDev)) {
            expenseAlertService.sendAlert("Anomalous expense detected!");
        }
    }
}