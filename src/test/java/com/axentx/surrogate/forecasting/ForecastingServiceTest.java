package com.axentx.surrogate.forecasting;

import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class ForecastingServiceTest {

    @Test
    public void testForecast() {
        ForecastingService forecastingService = new ForecastingService();
        List<Double> historicalData = Arrays.asList(10.0, 20.0, 30.0, 40.0, 50.0);
        int forecastPeriods = 3;

        ForecastResult result = forecastingService.forecast(historicalData, forecastPeriods);

        assertNotNull(result);
        assertEquals(forecastPeriods, result.getForecastPoints().size());

        for (ForecastPoint point : result.getForecastPoints()) {
            assertTrue(point.getValue() > 0);
            assertTrue(point.getLowerBound() < point.getValue());
            assertTrue(point.getUpperBound() > point.getValue());
        }
    }
}