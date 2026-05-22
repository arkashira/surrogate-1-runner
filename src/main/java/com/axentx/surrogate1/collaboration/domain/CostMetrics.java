package com.axentx.surrogate1.collaboration.domain;

import java.util.Map;

public final class CostMetrics {
    private final double total;
    private final Map<String, Double> byCategory;
    private final int count;

    public CostMetrics(double total, Map<String, Double> byCategory, int count) {
        this.total = total;
        this.byCategory = byCategory;
        this.count = count;
    }

    // getters …
}