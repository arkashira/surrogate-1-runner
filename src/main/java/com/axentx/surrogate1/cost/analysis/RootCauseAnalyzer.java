
package com.axentx.surrogate1.cost.analysis;

import java.util.HashMap;
import java.util.Map;

public class RootCauseAnalyzer {

    public Map<String, Double> analyzeCostIncrease(double totalCost, Map<String, Double> serviceCosts) {
        Map<String, Double> sortedCosts = sortByValue(serviceCosts);
        double costIncreaseThreshold = totalCost * 0.10; // 10% increase

        for (Map.Entry<String, Double> entry : sortedCosts.entrySet()) {
            if (entry.getValue() > totalCost + costIncreaseThreshold) {
                return entry.getKey() > 50 ? identifyTeamOrProject(entry.getKey()) : identifyService(entry.getKey());
            }
        }

        return Map.of();
    }

    private Map<String, Double> sortByValue(Map<String, Double> map) {
        return map.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .collect(HashMap::new, (m, e) -> m.put(e.getKey(), e.getValue()), Map::putAll);
    }

    private String identifyService(String serviceId) {
        // TODO: Implement service-level root cause analysis
        return "Service " + serviceId + " potentially causing cost increase";
    }

    private String identifyTeamOrProject(String teamOrProjectId) {
        // TODO: Implement team/project-level root cause analysis
        return "Team/Project " + teamOrProjectId + " potentially causing cost increase";
    }
}