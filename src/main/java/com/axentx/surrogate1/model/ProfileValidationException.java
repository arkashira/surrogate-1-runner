package com.axentx.surrogate1.model;

public class ProfileValidationException extends RuntimeException {

    public ProfileValidationException(String message) {
        super(message);
    }

    public ProfileValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}