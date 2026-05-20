package com.axentx.surrogate1.debugging;

import java.util.logging.Logger;

public class DebuggingTools {
    private static final Logger logger = Logger.getLogger(DebuggingTools.class.getName());

    public void enableDebugMode() {
        logger.info("Debug mode enabled");
        // Add debug mode implementation here
    }

    public void disableDebugMode() {
        logger.info("Debug mode disabled");
        // Add disable debug mode implementation here
    }

    public void printDebugInfo(String message) {
        logger.info("Debug info: " + message);
    }
}