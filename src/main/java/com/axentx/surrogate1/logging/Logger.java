package com.axentx.surrogate1.logging;

import java.util.logging.Level;
import java.util.logging.Logger;

public class Logger {
    private static final java.util.logging.Logger logger = java.util.logging.Logger.getLogger(Logger.class.getName());

    public static void logCriticalEvent(String message) {
        logger.log(Level.SEVERE, "CRITICAL EVENT: " + message);
    }

    public static void logError(String message, Throwable throwable) {
        logger.log(Level.SEVERE, "ERROR: " + message, throwable);
    }

    public static void logInfo(String message) {
        logger.log(Level.INFO, "INFO: " + message);
    }

    public static void logWarning(String message) {
        logger.log(Level.WARNING, "WARNING: " + message);
    }
}