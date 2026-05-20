package com.axentx.surrogate.llm;

/**
 * Runtime exception for LLM provider errors.
 */
public class LLMException extends Exception {
    public LLMException(String message) {
        super(message);
    }

    public LLMException(String message, Throwable cause) {
        super(message, cause);
    }
}