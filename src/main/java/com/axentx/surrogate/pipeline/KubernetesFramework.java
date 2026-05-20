package com.axentx.surrogate.pipeline;

import io.fabric8.kubernetes.api.model.Pod;

public class KubernetesFramework implements PipelineFramework {
    @Override
    public void integratePipeline(String pipelineConfig) {
        // TODO: parse pipelineConfig and create a Kubernetes Pod/Job
        System.out.println("Kubernetes: integrating pipeline config: " + pipelineConfig);
    }
}