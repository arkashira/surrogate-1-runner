package com.axentx.surrogate1.concurrency;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * RaceConditionDetector provides a lightweight runtime wrapper for {@link java.util.Map}
 * implementations (e.g., {@link java.util.concurrent.ConcurrentHashMap}) that logs
 * potential race conditions when the same key is accessed concurrently by multiple
 * threads. The detector is intentionally conservative: it logs a warning when
 * more than one thread is found to be operating on the same key simultaneously.
 *
 * <p>Usage example:
 * <pre>{@code
 * Map<String, Integer> original = new ConcurrentHashMap<>();
 * Map<String, Integer> monitored = RaceConditionDetector.wrap(original);
 * monitored.put("key", 1); // normal usage
 * }</pre>
 *
 * <p>Note: This detector does not guarantee detection of *all* race conditions
 * (e.g., compound operations like {@code putIfAbsent} followed by {@code get}).
 * It is intended as a quick sanity check during development.
 */
public final class RaceConditionDetector {

    private static final Logger LOGGER = Logger.getLogger(RaceConditionDetector.class.getName());

    /**
     * Internal tracking structure: for each wrapped map, maintain a mapping from key
     * to the set of thread IDs currently accessing that key.
     */
    private static final Map<Map<?, ?>, Map<Object, Set<Long>>> ACCESS_MAP = new ConcurrentHashMap<>();

    private RaceConditionDetector() {
        // Utility class
    }

    /**
     * Wraps the supplied {@link Map} with a proxy that monitors key access.
     *
     * @param <K> the type of keys
     * @param <V> the type of values
     * @param map the map to monitor
     * @return a proxy instance that implements {@link Map} and delegates to {@code map}
     */
    @SuppressWarnings("unchecked")
    public static <K, V> Map<K, V> wrap(Map<K, V> map) {
        if (map == null) {
            throw new IllegalArgumentException("Map cannot be null");
        }
        // Use the map itself as the key in ACCESS_MAP
        ACCESS_MAP.computeIfAbsent(map, k -> new ConcurrentHashMap<>());

        InvocationHandler handler = (proxy, method, args) -> {
            // Determine if the method operates on a key
            Object key = extractKey(method, args);
            if (key != null) {
                enter(map, key);
            }
            try {
                Object result = method.invoke(map, args);
                return result;
            } finally {
                if (key != null) {
                    exit(map, key);
                }
            }
        };

        return (Map<K, V>) Proxy.newProxyInstance(
                map.getClass().getClassLoader(),
                new Class<?>[]{Map.class},
                handler);
    }

    /**
     * Extracts the key argument from a {@link Map} method if applicable.
     *
     * @param method the invoked method
     * @param args   the method arguments
     * @return the key object or {@code null} if the method does not use a key
     */
    private static Object extractKey(Method method, Object[] args) {
        if (args == null || args.length == 0) {
            return null;
        }
        String name = method.getName();
        // Methods that use the first argument as a key
        switch (name) {
            case "get":
            case "put":
            case "remove":
            case "containsKey":
            case "replace":
            case "compute":
            case "computeIfAbsent":
            case "computeIfPresent":
            case "merge":
                return args[0];
            default:
                return null;
        }
    }

    /**
     * Records that the current thread has begun accessing {@code key} on {@code map}.
     *
     * @param map the wrapped map
     * @param key the key being accessed
     */
    private static void enter(Map<?, ?> map, Object key) {
        Map<Object, Set<Long>> keyMap = ACCESS_MAP.get(map);
        if (keyMap == null) {
            return;
        }
        Set<Long> threads = keyMap.computeIfAbsent(key, k -> ConcurrentHashMap.newKeySet());
        long threadId = Thread.currentThread().getId();
        threads.add(threadId);
        if (threads.size() > 1) {
            LOGGER.log(Level.WARNING,
                    "Potential race condition detected on key {0} in map {1}. Concurrent threads: {2}",
                    new Object[]{key, map, threads});
        }
    }

    /**
     * Records that the current thread has finished accessing {@code key} on {@code map}.
     *
     * @param map the wrapped map
     * @param key the key being accessed
     */
    private static void exit(Map<?, ?> map, Object key) {
        Map<Object, Set<Long>> keyMap = ACCESS_MAP.get(map);
        if (keyMap == null) {
            return;
        }
        Set<Long> threads = keyMap.get(key);
        if (threads == null) {
            return;
        }
        long threadId = Thread.currentThread().getId();
        threads.remove(threadId);
        if (threads.isEmpty()) {
            keyMap.remove(key);
        }
    }
}