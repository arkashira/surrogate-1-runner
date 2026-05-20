package com.axentx.surrogate.data;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

public class MarketingDataAnalyzerTest {
    @Test
    public void testAnalyzeMetrics() {
        MarketingDataAnalyzer analyzer = new MarketingDataAnalyzer();
        Map<String, Double> metrics = new HashMap<>();
        metrics.put("clickThroughRate", 0.01);
        metrics.put("conversionRate", 0.04);
        metrics.put("costPerClick", 0.6);

        String recommendations = analyzer.analyzeMetrics(metrics);

        assertTrue(recommendations.contains("Consider improving your ad targeting to increase click-through rate."));
        assertTrue(recommendations.contains("Review your landing page to improve conversion rate."));
        assertTrue(recommendations.contains("Consider optimizing your ad spend to reduce cost per click."));
    }
}