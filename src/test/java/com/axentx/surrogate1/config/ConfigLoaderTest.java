import com.axentx.surrogate1.config.ConfigLoader;
import org.junit.Test;

import java.util.Map;

import static org.junit.Assert.*;

public class ConfigLoaderTest {

    @Test
    public void testLoadConfig() {
        Map<String, String> config = ConfigLoader.loadConfig();
        assertNotNull(config);
    }

    @Test
    public void testValidateConfig() {
        Map<String, String> config = ConfigLoader.loadConfig();
        ConfigLoader.validateConfig(config);
    }

    @Test(expected = RuntimeException.class)
    public void testValidateConfigEmpty() {
        ConfigLoader.validateConfig(null);
    }

    @Test(expected = RuntimeException.class)
    public void testValidateConfigMissingApiKey() {
        Map<String, String> config = new HashMap<>();
        config.put("claude", null);
        ConfigLoader.validateConfig(config);
    }
}