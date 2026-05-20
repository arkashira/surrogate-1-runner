package com.axentx.surrogate1.cost.forecast;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ForecastGeneratorTest {

    @Test
    public void testGenerateForecasts() {
        List<ForecastGenerator.HistoricalCostData> historicalData = new ArrayList<>();
        historicalData.add(new ForecastGenerator.HistoricalCostData());
        // Populate historicalData with test data...

        ForecastGenerator generator = new ForecastGenerator();
        Map<String, Double> forecasts = generator.generateForecasts(historicalData, 30);

        assertEquals(1000.0 * 30, forecasts.get("ResourceA"), 0.001);
        assertEquals(1500.0 * 30, forecasts.get("ResourceB"), 0.001);
    }

    @Test
    public void testAdjustForecast() {
        Map<String, Double> forecasts = new HashMap<>();
        forecasts.put("ResourceA", 30000.0);
        forecasts.put("ResourceB", 45000.0);

        ForecastGenerator generator = new ForecastGenerator();
        generator.adjustForecast(forecasts, 1.1);

        assertEquals(33000.0, forecasts.get("ResourceA"), 0.001);
        assertEquals(49500.0, forecasts.get("ResourceB"), 0.001);
    }
}