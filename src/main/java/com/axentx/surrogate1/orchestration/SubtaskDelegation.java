package com.axentx.surrogate1.orchestration;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class SubtaskDelegation {

    private static final Map<String, Object> contextMap = new ConcurrentHashMap<>();

    public static void delegateSubtask(String subtaskName, Runnable subtask) {
        // Store current context before delegating
        String contextKey = generateContextKey(subtaskName);
        contextMap.put(contextKey, Thread.currentThread().getContextClassLoader());

        // Execute the subtask
        subtask.run();

        // Restore context after subtask execution
        Thread.currentThread().setContextClassLoader((ClassLoader) contextMap.get(contextKey));
    }

    private static String generateContextKey(String subtaskName) {
        return Thread.currentThread().getId() + "-" + subtaskName;
    }
}