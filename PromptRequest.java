package com.axentx.surrogate1.dto;

import java.util.Map;

public class PromptRequest {
    private String text;
    private Map<String, Object> structuredData;

    // Default constructor
    public PromptRequest() {}

    // Constructor accepting string prompt
    public PromptRequest(String text) {
        this.text = text;
    }

    // Constructor accepting structured data
    public PromptRequest(Map<String, Object> structuredData) {
        this.structuredData = structuredData;
    }

    // Getters and setters
    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public Map<String, Object> getStructuredData() {
        return structuredData;
    }

    public void setStructuredData(Map<String, Object> structuredData) {
        this.structuredData = structuredData;
    }
}