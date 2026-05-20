package com.axentx.surrogate.forecasting;

public class ForecastPoint {
    private int period;
    private double value;
    private double lowerBound;
    private double upperBound;

    public ForecastPoint(int period, double value, double lowerBound, double upperBound) {
        this.period = period;
        this.value = value;
        this.lowerBound = lowerBound;
        this.upperBound = upperBound;
    }

    public int getPeriod() {
        return period;
    }

    public double getValue() {
        return value;
    }

    public double getLowerBound() {
        return lowerBound;
    }

    public double getUpperBound() {
        return upperBound;
    }
}