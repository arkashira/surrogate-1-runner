package com.axentx.surrogate1.rightsize;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

class RightsizeServiceTest {

    @Test
    void testGetRecommendations() {
        RightsizeService service = new RightsizeService();
        List<Recommendation> recs = service.getRecommendations();

        assertNotNull(recs);
        assertEquals(2, recs.size());

        Recommendation first = recs.get(0);
        assertEquals("vm-frontend-01", first.getResourceId());
        assertEquals("t3.medium", first.getCurrentType());
        assertEquals("t3.large", first.getRecommendedType());
        assertEquals(0.12, first.getCurrentCostPerHour(), 0.001);
        assertEquals(0.24, first.getRecommendedCostPerHour(), 0.001);
        assertEquals(15.0, first.getCurrentCpuUsage(), 0.1);
        assertEquals(55.0, first.getRecommendedCpuUsage(), 0.1);
        assertEquals(0.12, first.getCostSavings(), 0.001);
        assertEquals(43.0, first.getPerformanceImpact(), 0.1);
    }
}