package com.axentx.surrogate1.analysis;

public final class Recommendation {
    private final String resourceId;
    private final String action;
    private final double potentialSavings;

    public Recommendation(String resourceId, String action, double potentialSavings) {
        this.resourceId = resourceId;
        this.action = action;
        this.potentialSavings = potentialSavings;
    }

    public String getResourceId() { return resourceId; }
    public String getAction() { return action; }
    public double getPotentialSavings() { return potentialSavings; }

    @Override
    public String toString() {
        return String.format("Resource: %s | Action: %s | Potential Savings: $%.2f",
                resourceId, action, potentialSavings);
    }
}