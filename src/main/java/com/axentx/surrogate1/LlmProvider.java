import java.util.function.Supplier;

public interface LlmProvider {
    boolean isAlive();
    String generateResponse(String input) throws Exception;
    default void onFailure(Supplier<RuntimeException> failure) {
        // Default failure handling
    }
}