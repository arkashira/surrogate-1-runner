package com.axentx.surrogate1.llm.template;

/**
 * Runtime exception thrown when an LLM provider fails to respond or returns
 * an error.  Providers should wrap lower‑level exceptions in this type.
 */
public class LLMProviderException extends RuntimeException {
    public LLMProviderException(String message) {
        super(message);
    }

    public LLMProviderException(String message, Throwable cause) {
        super(message, cause);
    }
}