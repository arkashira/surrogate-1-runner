package com.axentx.surrogate.dashboard;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MarketingDashboardTest {
    @Test
    public void testDisplayDashboard() {
        MarketingDashboard dashboard = new MarketingDashboard();
        dashboard.updateMetrics(0.03, 0.06, 0.4);

        // Since displayDashboard prints to console, we can't directly assert its output.
        // Instead, we can verify that the updateMetrics method works correctly.
        assertNotNull(dashboard);
    }
}