package com.axentx.surrogate.collections;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

public class ConcurrentCollectionUtils {

    /**
     * Default method to safely put an entry into a ConcurrentHashMap if it doesn't already exist.
     *
     * @param map   The ConcurrentHashMap instance.
     * @param key   The key of the entry to put.
     * @param value The value of the entry to put.
     * @param <K>   The type of keys maintained by this map.
     * @param <V>   The type of mapped values.
     */
    public static <K, V> void putIfAbsent(ConcurrentMap<K, V> map, K key, V value) {
        map.putIfAbsent(key, value);
    }

    /**
     * Default method to safely remove an entry from a ConcurrentHashMap if it exists.
     *
     * @param map The ConcurrentHashMap instance.
     * @param key The key of the entry to remove.
     * @param <K> The type of keys maintained by this map.
     * @param <V> The type of mapped values.
     */
    public static <K, V> void removeIfExists(ConcurrentMap<K, V> map, K key) {
        map.remove(key);
    }
}