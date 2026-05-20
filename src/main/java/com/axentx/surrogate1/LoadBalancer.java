import java.util.List;

public class LoadBalancer {
    private List<LlmProvider> providers;

    public LoadBalancer(List<LlmProvider> providers) {
        this.providers = providers;
    }

    public LlmProvider getProvider() {
        // Implement load-balancing logic here
        // For example, you can use a round-robin algorithm
        int index = 0;
        return providers.get(index++);
    }
}