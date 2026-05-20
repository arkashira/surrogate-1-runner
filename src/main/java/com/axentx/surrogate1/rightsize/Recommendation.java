package com.axentx.surrogate1.rightsize;

public class Recommendation {
    private final String resourceId;
    private final String currentType;
    private final String recommendedType;
    private final double currentCostPerHour;
    private final double recommendedCostPerHour;
    private final double currentCpuUsage;
    private final double recommendedCpuUsage;
    private final double costSavings;
    private final double performanceImpact;

    public Recommendation(String resourceId, String currentType, String recommendedType,
                          double currentCostPerHour, double recommendedCostPerHour,
                          double currentCpuUsage, double recommendedCpuUsage,
                          double costSavings, double performanceImpact) {
        this.resourceId = resourceId;
        this.currentType = currentType;
        this.recommendedType = recommendedType;
        this.currentCostPerHour = currentCostPerHour;
        this.recommendedCostPerHour = recommendedCostPerHour;
        this.currentCpuUsage = currentCpuUsage;
        this.recommendedCpuUsage = recommendedCpuUsage;
        this.costSavings = costSavings;
        this.performanceImpact = performanceImpact;
    }

    // Getters

    @Override
    public String toString() {
        return "Recommendation{" +
                "resourceId='" + resourceId + '\'' +
                ", currentType='" + currentType + '\'' +
                ", recommendedType='" + recommendedType + '\'' +
                ", currentCostPerHour=" + currentCostPerHour +
                ", recommendedCostPerHour=" + recommendedCostPerHour +
                ", currentCpuUsage=" + currentCpuUsage +
                ", recommendedCpuUsage=" + recommendedCpuUsage +
                ", costSavings=" + costSavings +
                ", performanceImpact=" + performanceImpact +
                '}';
    }
}