package com.axentx.surrogate.pipeline;

import org.apache.airflow.models.DAG;

public class ApacheAirflowFramework implements PipelineFramework {
    @Override
    public void integratePipeline(String pipelineConfig) {
        // TODO: parse pipelineConfig and create an Airflow DAG
        // For demo purposes we just log the action
        System.out.println("Airflow: integrating pipeline config: " + pipelineConfig);
    }
}