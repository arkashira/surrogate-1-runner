package com.axentx.surrogate.model;

public class SurrogateModel {
    private String modelId;

    public SurrogateModel(String modelId) {
        this.modelId = modelId;
    }

    public String invoke(SurrogatePrompt prompt, SurrogateOptions options) throws Exception {
        // implementation of the Surrogate-1 LLM model invocation
        // this is a placeholder, actual implementation should be provided
        return "response from Surrogate-1 LLM model";
    }
}