package com.axentx.surrogate1.config;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api")
public class ConfigController {

    private final ConfigService configService;

    public ConfigController(ConfigService configService) {
        this.configService = configService;
    }

    /**
     * Returns the configuration JSON. Any query parameter supplied will
     * override the corresponding default value. Unknown parameters are
     * accepted as custom configuration entries.
     *
     * @param overrides all query parameters supplied by the caller
     * @return a map containing {@code defaults}, {@code config} and {@code overridden}
     */
    @GetMapping("/config")
    public Map<String, Object> getConfig(@RequestParam Map<String, String> overrides) {
        return configService.getConfig(overrides);
    }

    @PostMapping("/config")
    public Map<String, Object> setConfig(@RequestBody Map<String, String> configOverride) {
        return configService.setOverrideConfig(configOverride);
    }
}

class ConfigService {
    private static final Map<String, String> DEFAULTS;
    static {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("autoDetect", "true");
        map.put("maxWorkers", "16");
        map.put("datasetPath", "/data/dataset");
        DEFAULTS = Collections.unmodifiableMap(map);
    }

    private Map<String, String> currentConfig = new LinkedHashMap<>(DEFAULTS);

    public Map<String, Object> getConfig(Map<String, String> overrides) {
        Map<String, String> effective = new LinkedHashMap<>(currentConfig);
        Set<String> overriddenKeys = new HashSet<>();

        for (Map.Entry<String, String> entry : overrides.entrySet()) {
            effective.put(entry.getKey(), entry.getValue());
            overriddenKeys.add(entry.getKey());
        }

        Map<String, Object> response = new HashMap<>();
        response.put("defaults", DEFAULTS);
        response.put("config", effective);
        response.put("overridden", overriddenKeys);
        return response;
    }

    public Map<String, Object> setOverrideConfig(Map<String, String> configOverride) {
        for (Map.Entry<String, String> entry : configOverride.entrySet()) {
            currentConfig.put(entry.getKey(), entry.getValue());
        }
        return getConfig(Collections.emptyMap());
    }
}