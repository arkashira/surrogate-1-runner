
package com.axentx.surrogate1.api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.stream.Collectors;

@RestController
public class FinancialDataAggregator {

    private final FinancialDataRepository financialDataRepository;

    public FinancialDataAggregator(FinancialDataRepository financialDataRepository) {
        this.financialDataRepository = financialDataRepository;
    }

    @GetMapping("/api/financial-data/aggregate")
    public AggregatedFinancialData aggregateData(
            @RequestParam(value = "source") String source,
            @RequestParam(value = "startDate") LocalDate startDate,
            @RequestParam(value = "endDate") LocalDate endDate) {

        List<FinancialData> dataList = financialDataRepository.findBySource(source)
                .stream()
                .filter(fd -> fd.getDate().isAfter(startDate))
                .filter(fd -> fd.getDate().isBefore(endDate.plusDays(1)))
                .collect(Collectors.toList());

        double revenue = dataList.stream()
                .mapToDouble(FinancialData::getRevenue)
                .sum();

        double expense = dataList.stream()
                .mapToDouble(FinancialData::getExpense)
                .sum();

        double dailyRevenue = revenue / ChronoUnit.DAYS.between(startDate, endDate);
        double dailyExpense = expense / ChronoUnit.DAYS.between(startDate, endDate);

        return new AggregatedFinancialData(
                startDate,
                endDate,
                dailyRevenue,
                dailyExpense,
                calculateAlerts(dailyRevenue, dailyExpense)
        );
    }

    private List<Alert> calculateAlerts(double dailyRevenue, double dailyExpense) {
        // Implement logic for color-coded alerts based on dailyRevenue and dailyExpense
        // ...
        return null; // Placeholder, implement this logic
    }
}

# src/main/java/com/axentx/surrogate1/domain/AggregatedFinancialData.java

package com.axentx.surrogate1.domain;

public record AggregatedFinancialData(
        LocalDate startDate,
        LocalDate endDate,
        double dailyRevenue,
        double dailyExpense,
        List<Alert> alerts
) {
}

# src/main/java/com/axentx/surrogate1/domain/Alert.java

package com.axentx.surrogate1.domain;

public enum Alert {
    GREEN,
    YELLOW,
    RED;
}