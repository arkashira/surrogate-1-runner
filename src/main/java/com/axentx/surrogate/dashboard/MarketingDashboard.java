package com.axentx.surrogate.dashboard;

import com.axentx.surrogate.data.MarketingDataAnalyzer;
import com.axentx.surrogate.data.MarketingDataCollector;

import java.util.Map;

public class MarketingDashboard {
    private MarketingDataCollector collector;
    private MarketingDataAnalyzer analyzer;

    public MarketingDashboard() {
        this.collector = new MarketingDataCollector();
        this.analyzer = new MarketingDataAnalyzer();
    }

    public void updateMetrics(double ctr, double cr, double cpc) {
        collector.collectClickThroughRate(ctr);
        collector.collectConversionRate(cr);
        collector.collectCostPerClick(cpc);
    }

    public void displayDashboard() {
        Map<String, Double> metrics = collector.getMetrics();
        String recommendations = analyzer.analyzeMetrics(metrics);

        System.out.println("Marketing Performance Dashboard");
        System.out.println("--------------------------------");
        System.out.println("Click-Through Rate: " + metrics.get("clickThroughRate"));
        System.out.println("Conversion Rate: " + metrics.get("conversionRate"));
        System.out.println("Cost Per Click: " + metrics.get("costPerClick"));
        System.out.println("\nRecommendations:");
        System.out.println(recommendations);
    }
}