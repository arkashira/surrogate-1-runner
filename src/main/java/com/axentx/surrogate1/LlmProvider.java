import java.util.HashMap;
import java.util.Map;

import com.axentx.surrogate1.LlmProviderMetrics;

public class LlmProvider {
    private String name;
    private Map<String, Double> metrics;

    public LlmProvider(String name) {
        this.name = name;
        this.metrics = new HashMap<>();
    }

    public LlmProviderMetrics getMetrics() {
        LlmProviderMetrics metrics = new LlmProviderMetrics();
        metrics.setName(name);
        metrics.setLatency(this.metrics.get("latency"));
        metrics.setCost(this.metrics.get("cost"));
        metrics.setErrorRate(this.metrics.get("errorRate"));
        return metrics;
    }

    public void updateMetrics() {
        // Simulate API call to llm-orchestra API
        // Replace with actual API call
        this.metrics.put("latency", 10.0);
        this.metrics.put("cost", 5.0);
        this.metrics.put("errorRate", 0.01);
    }
}