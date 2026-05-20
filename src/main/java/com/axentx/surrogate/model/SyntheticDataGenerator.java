package com.axentx.surrogate.model;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class SyntheticDataGenerator {

    private final Map<String, String> integrationDataGenerators;

    public SyntheticDataGenerator() {
        integrationDataGenerators = new HashMap<>();
        integrationDataGenerators.put("datadog", this::generateDatadogData);
    }

    public String generate(String integrationType) {
        if (integrationDataGenerators.containsKey(integrationType)) {
            return integrationDataGenerators.get(integrationType).get();
        }
        throw new IllegalArgumentException("Unsupported integration type: " + integrationType);
    }

    private String generateDatadogData() {
        Random random = new Random();
        int metricValue = random.nextInt(100);
        return String.format("{\"metric\": \"datadog.metric\", \"value\": %d}", metricValue);
    }
}