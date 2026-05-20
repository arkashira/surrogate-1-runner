import com.axentx.surrogate1.LlmProvider;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

public class LlmOrchestrator {
    private final List<LlmProvider> providers;

    public LlmOrchestrator(List<LlmProvider> providers) {
        this.providers = providers;
    }

    public String getResponse(String input) {
        AtomicReference<String> response = new AtomicReference<>();
        providers.stream()
                  .filter(LlmProvider::isAlive)
                  .forEach(provider -> {
                      try {
                          String result = provider.generateResponse(input);
                          if (result != null) {
                              response.set(result);
                          }
                      } catch (Exception e) {
                          // Handle or log exception
                      }
                  });
        return response.get();
    }
}