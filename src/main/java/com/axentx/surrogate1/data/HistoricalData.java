package com.axentx.surrogate1.data;

public class HistoricalData {
    private final double averageUsage;
    private final double standardDeviation;

    public HistoricalData(double averageUsage, double standardDeviation) {
        this.averageUsage = averageUsage;
        this.standardDeviation = standardDeviation;
    }

    public double getAverageUsage() {
        return averageUsage;
    }

    public double getStandardDeviation() {
        return standardDeviation;
    }
}