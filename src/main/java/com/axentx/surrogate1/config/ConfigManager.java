import com.axentx.surrogate1.config.ConfigDetector;
import com.axentx.surrogate1.config.ConfigOverride;

public class ConfigManager {
    public static Map<String, Object> getConfig() throws Exception {
        Map<String, Object> config = ConfigDetector.detectConfig();
        ConfigOverride override = new ConfigOverride(config);
        // Add override logic here
        return override.getConfig();
    }
}