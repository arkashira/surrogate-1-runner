package com.axentx.surrogate.collections;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

import static org.junit.jupiter.api.Assertions.*;

public class ConcurrentCollectionUtilsTest {

    @Test
    public void testPutIfAbsent() {
        ConcurrentMap<String, String> map = new ConcurrentHashMap<>();
        ConcurrentCollectionUtils.putIfAbsent(map, "key", "value");
        assertEquals("value", map.get("key"));

        // Ensure it doesn't overwrite existing values
        ConcurrentCollectionUtils.putIfAbsent(map, "key", "new_value");
        assertEquals("value", map.get("key"));
    }

    @Test
    public void testRemoveIfExists() {
        ConcurrentMap<String, String> map = new ConcurrentHashMap<>();
        map.put("key", "value");

        ConcurrentCollectionUtils.removeIfExists(map, "key");
        assertFalse(map.containsKey("key"));

        // Ensure it doesn't throw an exception when removing non-existent keys
        ConcurrentCollectionUtils.removeIfExists(map, "nonexistent_key");
    }
}