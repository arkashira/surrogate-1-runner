package com.axentx.surrogate1.performance;

import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PerformanceLogger {
    private static final Logger logger = Logger.getLogger(PerformanceLogger.class.getName());
    private static final ConcurrentHashMap<String, Long> performanceMetrics = new ConcurrentHashMap<>();

    public static void logPerformanceBottleneck(String collectionName, long executionTime) {
        performanceMetrics.put(collectionName, executionTime);
        logger.log(Level.WARNING, "Performance bottleneck detected in {0}. Execution time: {1} ms", new Object[]{collectionName, executionTime});
    }

    public static void reportPerformanceBottlenecks() {
        performanceMetrics.forEach((collectionName, executionTime) -> {
            if (executionTime > 1000) { // Assuming 1000ms as a threshold for performance bottleneck
                logger.log(Level.SEVERE, "Performance bottleneck report: Collection {0} took {1} ms", new Object[]{collectionName, executionTime});
                recommendEfficientCollection(collectionName);
            }
        });
    }

    private static void recommendEfficientCollection(String collectionName) {
        logger.log(Level.INFO, "Recommendation for {0}: Consider using a different concurrent collection implementation for better performance.", collectionName);
    }
}