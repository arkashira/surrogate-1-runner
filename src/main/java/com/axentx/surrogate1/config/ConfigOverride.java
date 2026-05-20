import java.util.Map;

public class ConfigOverride {
    private Map<String, Object> config;

    public ConfigOverride(Map<String, Object> config) {
        this.config = config;
    }

    public void override(String key, Object value) {
        config.put(key, value);
    }

    public Map<String, Object> getConfig() {
        return config;
    }
}