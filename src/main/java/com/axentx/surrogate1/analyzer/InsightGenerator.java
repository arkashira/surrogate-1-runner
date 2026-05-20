package com.axentx.surrogate1.analyzer;

import java.util.List;
import java.util.Map;

public class InsightGenerator {
    private ConcurrentCollectionAnalyzer analyzer;

    public InsightGenerator(ConcurrentCollectionAnalyzer analyzer) {
        this.analyzer = analyzer;
    }

    public List<String> generateInsights(Map<String, Object> issueDetails) {
        List<String> insights = new java.util.ArrayList<>();
        String issueType = (String) issueDetails.get("type");

        switch (issueType) {
            case "RaceCondition":
                insights.add("Ensure proper synchronization mechanisms like locks or atomic operations.");
                break;
            case "Deadlock":
                insights.add("Review lock ordering and consider using tryLock() with a timeout.");
                break;
            case "Starvation":
                insights.add("Implement fair scheduling policies and monitor thread priorities.");
                break;
            default:
                insights.add("General advice: Review concurrency patterns and ensure thread safety.");
        }

        return insights;
    }
}