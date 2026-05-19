// File: src/main/java/com/axentx/surrogate1/orchestration/ContextManager.java
package com.axentx.surrogate1.orchestration;

import java.util.Collections;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * A lightweight, thread‑safe context holder that allows arbitrary key/value
 * pairs to be stored and passed between agents in a workflow.
 *
 * <p>Contexts can be nested by passing a parent {@code ContextManager} to the
 * constructor. All values from the parent are copied into the new instance
 * and can be overridden by child values.</p>
 *
 * <p>All operations are O(1) and the internal map is a {@link ConcurrentHashMap}
 * to support concurrent reads/writes from multiple agents.</p>
 */
public final class ContextManager {

    private final ConcurrentHashMap<String, Object> contextMap;

    /* ------------------------------------------------------------------ */
    /* Constructors                                                        */
    /* ------------------------------------------------------------------ */

    /** Create an empty context. */
    public ContextManager() {
        this.contextMap = new ConcurrentHashMap<>();
    }

    /**
     * Create a new context that inherits all key/value pairs from the given
     * parent context. Child values can override parent values.
     *
     * @param parent the parent context to inherit from; may be {@code null}
     */
    public ContextManager(ContextManager parent) {
        this();
        if (parent != null) {
            this.contextMap.putAll(parent.contextMap);
        }
    }

    /* ------------------------------------------------------------------ */
    /* Core API                                                            */
    /* ------------------------------------------------------------------ */

    /**
     * Store a key/value pair in the context. If the key already exists,
     * its value is replaced.
     *
     * @param key   the key; must not be {@code null}
     * @param value the value; may be {@code null}
     */
    public void put(String key, Object value) {
        if (key == null) {
            throw new IllegalArgumentException("Context key cannot be null");
        }
        contextMap.put(key, value);
    }

    /**
     * Retrieve the value associated with the given key.
     *
     * @param key the key; must not be {@code null}
     * @return the value, or {@code null} if the key is not present
     */
    public Object get(String key) {
        if (key == null) {
            throw new IllegalArgumentException("Context key cannot be null");
        }
        return contextMap.get(key);
    }

    /**
     * Return an unmodifiable view of the entire context map.
     *
     * @return an unmodifiable {@link Map} containing all key/value pairs
     */
    public Map<String, Object> getAll() {
        return Collections.unmodifiableMap(contextMap);
    }

    /**
     * Merge another context into this one. Existing keys are overridden by
     * values from the other context.
     *
     * @param other the other context to merge; may be {@code null}
     */
    public void merge(ContextManager other) {
        if (other == null) {
            return;
        }
        contextMap.putAll(other.contextMap);
    }

    /**
     * Create a deep copy of this context. The returned instance is completely
     * independent of the original.
     *
     * @return a new {@link ContextManager} containing the same key/value pairs
     */
    public ContextManager copy() {
        ContextManager copy = new ContextManager();
        copy.contextMap.putAll(this.contextMap);
        return copy;
    }

    /* ------------------------------------------------------------------ */
    /* Utility & Debugging                                               */
    /* ------------------------------------------------------------------ */

    @Override
    public String toString() {
        return "ContextManager" + contextMap.toString();
    }
}