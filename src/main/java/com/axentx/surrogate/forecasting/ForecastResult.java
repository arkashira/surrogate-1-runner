package com.axentx.surrogate.forecasting;

import java.util.ArrayList;
import java.util.List;

public class ForecastResult {
    private double slope;
    private double intercept;
    private List<ForecastPoint> forecastPoints;

    public ForecastResult() {
        this.forecastPoints = new ArrayList<>();
    }

    public double getSlope() {
        return slope;
    }

    public void setSlope(double slope) {
        this.slope = slope;
    }

    public double getIntercept() {
        return intercept;
    }

    public void setIntercept(double intercept) {
        this.intercept = intercept;
    }

    public List<ForecastPoint> getForecastPoints() {
        return forecastPoints;
    }

    public void addForecast(ForecastPoint point) {
        this.forecastPoints.add(point);
    }
}