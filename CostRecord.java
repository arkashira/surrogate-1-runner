package com.axentx.surrogate1.analysis;

public final class CostRecord {
    private final String resourceId;
    private final double cost;   // cost for a single day (or any period)

    public CostRecord(String resourceId, double cost) {
        this.resourceId = resourceId;
        this.cost = cost;
    }

    public String getResourceId() { return resourceId; }
    public double getCost() { return cost; }
}