import java.util.ArrayList;
import java.util.List;

import com.axentx.surrogate1.LlmProvider;
import com.axentx.surrogate1.LlmProviderMetrics;

public class LlmOrchestrator {
    private List<LlmProvider> providers;

    public LlmOrchestrator() {
        this.providers = new ArrayList<>();
    }

    public void addProvider(LlmProvider provider) {
        this.providers.add(provider);
    }

    public List<LlmProviderMetrics> getMetrics() {
        List<LlmProviderMetrics> metrics = new ArrayList<>();
        for (LlmProvider provider : providers) {
            metrics.add(provider.getMetrics());
        }
        return metrics;
    }

    public void updateMetrics() {
        for (LlmProvider provider : providers) {
            provider.updateMetrics();
        }
    }
}