
package com.axentx.surrogate.collections;

import org.junit.Test;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentSkipListSet;

import static org.junit.Assert.assertEquals;

public class SynchronizedCollectionsTest {

    @Test
    public void testConcurrentHashMap() {
        ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
        map.putIfAbsent("key", "value");
        map.putIfAbsent("key", "newValue"); // should not override
        assertEquals("value", map.get("key"));
    }

    @Test
    public void testConcurrentSkipListSet() {
        ConcurrentSkipListSet<String> set = new ConcurrentSkipListSet<>();
        set.add("element");
        set.add("element"); // should not override
        assertEquals(1, set.size());
    }
}