package com.axentx.surrogate1.analyzer;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class RecommendationEngine {
    private final ConcurrentCollectionAnalyzer collectionAnalyzer;

    public RecommendationEngine() {
        this.collectionAnalyzer = new ConcurrentCollectionAnalyzer();
    }

    public Map<String, String> analyzeAndRecommend(String code) {
        Map<String, String> recommendations = new HashMap<>();
        List<String> collectionUsages = collectionAnalyzer.analyzeCollections(code);

        for (String usage : collectionUsages) {
            String recommendation = generateRecommendation(usage);
            if (recommendation != null) {
                recommendations.put(usage, recommendation);
            }
        }

        return recommendations;
    }

    private String generateRecommendation(String collectionUsage) {
        // Implement logic to generate recommendations based on collection usage
        // This is a simplified example
        if (collectionUsage.contains("ArrayList") && collectionUsage.contains("frequent access")) {
            return "Consider using LinkedList for frequent access operations";
        } else if (collectionUsage.contains("HashMap") && collectionUsage.contains("concurrent access")) {
            return "Consider using ConcurrentHashMap for concurrent access";
        }
        // Add more recommendations as needed
        return null;
    }
}