import java.util.HashMap;
import java.util.Map;

public class ConfigLoader {
    private static final String Claude_API_KEY = "CLAUDE_API_KEY";
    private static final String Minimax_API_KEY = "MINIMAX_API_KEY";
    private static final String OpenAI_API_KEY = "OPENAI_API_KEY";
    private static final String Anthropic_API_KEY = "ANTHROPIC_API_KEY";
    private static final String Cohere_API_KEY = "COHERE_API_KEY";
    private static final String Gemini_API_KEY = "GEMINI_API_KEY";

    public static Map<String, String> loadConfig() {
        Map<String, String> config = new HashMap<>();
        config.put("claude", System.getenv(Claude_API_KEY));
        config.put("minimax", System.getenv(Minimax_API_KEY));
        config.put("openai", System.getenv(OpenAI_API_KEY));
        config.put("anthropic", System.getenv(Anthropic_API_KEY));
        config.put("cohere", System.getenv(Cohere_API_KEY));
        config.put("gemini", System.getenv(Gemini_API_KEY));
        return config;
    }

    public static void validateConfig(Map<String, String> config) {
        if (config == null || config.isEmpty()) {
            throw new RuntimeException("No configuration found");
        }
        for (Map.Entry<String, String> entry : config.entrySet()) {
            if (entry.getValue() == null || entry.getValue().isEmpty()) {
                throw new RuntimeException("Missing API key for " + entry.getKey());
            }
        }
    }
}