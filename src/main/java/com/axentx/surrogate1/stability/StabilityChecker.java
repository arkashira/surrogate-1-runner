package com.axentx.surrogate1.stability;

import java.util.concurrent.atomic.AtomicBoolean;

public class StabilityChecker {
    private static final AtomicBoolean isSystemStable = new AtomicBoolean(true);

    public static boolean checkSystemStability() {
        // Simulate checking various system metrics like temperature, memory usage, etc.
        // For demonstration purposes, we'll just return the current state.
        return isSystemStable.get();
    }

    public static void adjustSystemStability(boolean stable) {
        isSystemStable.set(stable);
    }
}