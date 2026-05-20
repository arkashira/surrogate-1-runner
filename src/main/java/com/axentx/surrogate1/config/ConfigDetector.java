import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

public class ConfigDetector {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static Map<String, Object> detectConfig() throws IOException {
        Path configPath = Paths.get("src/main/resources/config/defaults.json");
        if (Files.exists(configPath)) {
            return MAPPER.readValue(configPath.toFile(), Map.class);
        } else {
            return new HashMap<>();
        }
    }
}