package com.axentx.surrogate1.cost.forecast;

import java.util.List;
import java.util.Map;

public class ForecastGenerator {

    private static final int DEFAULT_FORECAST_PERIOD = 30; // days

    public Map<String, Double> generateForecasts(List<HistoricalCostData> historicalData, int forecastPeriod) {
        if (historicalData == null || historicalData.isEmpty()) {
            throw new IllegalArgumentException("Historical data cannot be null or empty");
        }

        forecastPeriod = forecastPeriod > 0 ? forecastPeriod : DEFAULT_FORECAST_PERIOD;

        return calculatePredictiveCosts(historicalData, forecastPeriod);
    }

    private Map<String, Double> calculatePredictiveCosts(List<HistoricalCostData> historicalData, int forecastPeriod) {
        // Placeholder for actual forecasting logic using historical data
        // This could involve statistical models, machine learning, etc.
        // For simplicity, we'll just return a mock map here.
        Map<String, Double> forecasts = new java.util.HashMap<>();
        forecasts.put("ResourceA", 1000.0 * forecastPeriod);
        forecasts.put("ResourceB", 1500.0 * forecastPeriod);
        return forecasts;
    }

    public void adjustForecast(Map<String, Double> forecasts, double adjustmentFactor) {
        if (forecasts == null || forecasts.isEmpty()) {
            throw new IllegalArgumentException("Forecasts cannot be null or empty");
        }

        for (Map.Entry<String, Double> entry : forecasts.entrySet()) {
            entry.setValue(entry.getValue() * adjustmentFactor);
        }
    }

    public static class HistoricalCostData {
        private String resourceId;
        private double cost;
        private long timestamp;

        // Constructor, getters, setters...
    }
}