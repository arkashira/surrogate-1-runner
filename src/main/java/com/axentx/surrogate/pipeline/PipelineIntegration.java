package com.axentx.surrogate.pipeline;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class PipelineIntegration {

    private final Map<String, PipelineFramework> frameworks = new ConcurrentHashMap<>();

    public void registerFramework(String name, PipelineFramework framework) {
        frameworks.put(name.toLowerCase(), framework);
    }

    public PipelineFramework getFramework(String name) {
        return frameworks.get(name.toLowerCase());
    }

    public void integratePipeline(String frameworkName, String pipelineConfig) {
        PipelineFramework framework = getFramework(frameworkName);
        if (framework == null) {
            throw new IllegalArgumentException("Unsupported framework: " + frameworkName);
        }
        framework.integratePipeline(pipelineConfig);
    }
}