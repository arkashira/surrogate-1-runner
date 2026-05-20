package com.axentx.surrogate1.detection;

import java.util.Map;
import java.util.HashMap;

public class ConfigDriftDetector {

    private Map<String, String> baselineConfigurations;

    public ConfigDriftDetector() {
        this.baselineConfigurations = new HashMap<>();
    }

    public void setBaselineConfiguration(String resourceId, String config) {
        baselineConfigurations.put(resourceId, config);
    }

    public boolean detectDrift(String resourceId, String currentConfig) {
        String baselineConfig = baselineConfigurations.get(resourceId);
        return !currentConfig.equals(baselineConfig);
    }

    public String getRemediationSuggestion(String resourceId, String currentConfig) {
        String baselineConfig = baselineConfigurations.get(resourceId);
        if (baselineConfig == null) {
            return "No baseline configuration found for resource.";
        }
        return "Revert configuration to: " + baselineConfig;
    }
}