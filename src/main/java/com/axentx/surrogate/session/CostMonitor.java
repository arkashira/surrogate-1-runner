
package com.axentx.surrogate.session;

import org.costinel.Costinel;
import org.costinel.CostinelClient;
import org.costinel.CostinelConfig;

public class CostMonitor {
    private static final CostinelClient costinelClient = new CostinelClient(
            new CostinelConfig("your_costinel_api_key"));

    public void recordSessionCost(double cost) {
        costinelClient.recordCost(cost);
    }
}