package com.axentx.surrogate1.llm.template;

/**
 * Simple DTO representing a parsed LLM response.  Providers may extend this
 * class or replace it with a richer implementation.
 */
public class ParsedResponse {
    private final String content;

    public ParsedResponse(String content) {
        this.content = content;
    }

    public String getContent() {
        return content;
    }
}