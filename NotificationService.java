package com.axentx.surrogate1;

/** Simple unchecked wrapper for any delivery problem. */
public class NotificationException extends RuntimeException {
    public NotificationException(String msg, Throwable cause) {
        super(msg, cause);
    }
}