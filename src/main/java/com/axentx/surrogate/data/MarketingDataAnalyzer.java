package com.axentx.surrogate.data;

import java.util.Map;

public class MarketingDataAnalyzer {
    public String analyzeMetrics(Map<String, Double> metrics) {
        StringBuilder recommendations = new StringBuilder();

        double ctr = metrics.getOrDefault("clickThroughRate", 0.0);
        double cr = metrics.getOrDefault("conversionRate", 0.0);
        double cpc = metrics.getOrDefault("costPerClick", 0.0);

        if (ctr < 0.02) {
            recommendations.append("Consider improving your ad targeting to increase click-through rate.\n");
        }

        if (cr < 0.05) {
            recommendations.append("Review your landing page to improve conversion rate.\n");
        }

        if (cpc > 0.5) {
            recommendations.append("Consider optimizing your ad spend to reduce cost per click.\n");
        }

        return recommendations.toString();
    }
}