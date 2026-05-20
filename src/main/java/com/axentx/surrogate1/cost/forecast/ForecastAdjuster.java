package com.axentx.surrogate1.cost.forecast;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

public class ForecastAdjuster {
    
    /**
     * Adjusts a cost forecast based on projected usage changes
     * @param originalForecast the original forecast data
     * @param adjustments map of date to adjustment percentage (e.g., 1.10 for 10% increase)
     * @return adjusted forecast data
     */
    public Map<LocalDate, BigDecimal> adjustForecast(
            Map<LocalDate, BigDecimal> originalForecast, 
            Map<LocalDate, Double> adjustments) {
        
        // Create a copy of the original forecast to avoid modifying it directly
        Map<LocalDate, BigDecimal> adjustedForecast = new java.util.HashMap<>(originalForecast);
        
        // Apply adjustments to each date in the forecast
        for (Map.Entry<LocalDate, Double> adjustment : adjustments.entrySet()) {
            LocalDate date = adjustment.getKey();
            Double adjustmentFactor = adjustment.getValue();
            
            if (adjustedForecast.containsKey(date)) {
                BigDecimal originalValue = adjustedForecast.get(date);
                BigDecimal adjustedValue = originalValue.multiply(BigDecimal.valueOf(adjustmentFactor));
                adjustedForecast.put(date, adjustedValue);
            }
        }
        
        return adjustedForecast;
    }
    
    /**
     * Applies a global multiplier to all forecast values
     * @param originalForecast the original forecast data
     * @param multiplier the factor by which to multiply all values
     * @return adjusted forecast data
     */
    public Map<LocalDate, BigDecimal> applyGlobalMultiplier(
            Map<LocalDate, BigDecimal> originalForecast, 
            double multiplier) {
        
        Map<LocalDate, BigDecimal> adjustedForecast = new java.util.HashMap<>();
        
        for (Map.Entry<LocalDate, BigDecimal> entry : originalForecast.entrySet()) {
            BigDecimal adjustedValue = entry.getValue().multiply(BigDecimal.valueOf(multiplier));
            adjustedForecast.put(entry.getKey(), adjustedValue);
        }
        
        return adjustedForecast;
    }
}