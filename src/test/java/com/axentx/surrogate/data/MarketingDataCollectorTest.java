package com.axentx.surrogate.data;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MarketingDataCollectorTest {
    @Test
    public void testCollectMetrics() {
        MarketingDataCollector collector = new MarketingDataCollector();
        collector.collectClickThroughRate(0.03);
        collector.collectConversionRate(0.06);
        collector.collectCostPerClick(0.4);

        assertEquals(0.03, collector.getMetrics().get("clickThroughRate"));
        assertEquals(0.06, collector.getMetrics().get("conversionRate"));
        assertEquals(0.4, collector.getMetrics().get("costPerClick"));
    }
}