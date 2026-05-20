package com.axentx.surrogate.data;

import java.util.HashMap;
import java.util.Map;

public class MarketingDataCollector {
    private Map<String, Double> metrics;

    public MarketingDataCollector() {
        this.metrics = new HashMap<>();
    }

    public void collectClickThroughRate(double ctr) {
        metrics.put("clickThroughRate", ctr);
    }

    public void collectConversionRate(double cr) {
        metrics.put("conversionRate", cr);
    }

    public void collectCostPerClick(double cpc) {
        metrics.put("costPerClick", cpc);
    }

    public Map<String, Double> getMetrics() {
        return metrics;
    }
}