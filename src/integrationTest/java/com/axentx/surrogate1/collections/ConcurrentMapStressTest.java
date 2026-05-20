package com.axentx.surrogate1.collections;

import org.junit.jupiter.api.Test;
import java.util.concurrent.*;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.*;

public class ConcurrentMapStressTest {

    private static final int THREAD_COUNT = 100;
    private static final int ITERATIONS_PER_THREAD = 1000;

    @Test
    public void testConcurrentOperations() throws InterruptedException {
        ThreadSafeMap<String, String> map = new ThreadSafeMap<>();

        CyclicBarrier barrier = new CyclicBarrier(THREAD_COUNT);

        ExecutorService executor = Executors.newFixedThreadPool(THREAD_COUNT);
        IntStream.range(0, THREAD_COUNT).forEach(i -> {
            executor.submit(() -> {
                try {
                    barrier.await();
                    for (int j = 0; j < ITERATIONS_PER_THREAD; j++) {
                        map.put("key-" + i + "-" + j, "value-" + i + "-" + j);
                        map.computeIfAbsent("compute-key-" + i + "-" + j, k -> "computed-value-" + i + "-" + j);
                        map.replaceAll((k, v) -> v + "-updated");
                    }
                } catch (InterruptedException | BrokenBarrierException e) {
                    Thread.currentThread().interrupt();
                    fail("Thread interrupted", e);
                }
            });
        });

        executor.shutdown();
        assertTrue(executor.awaitTermination(1, TimeUnit.MINUTES));

        // Verify the map size after all threads have completed their operations
        assertEquals(THREAD_COUNT * ITERATIONS_PER_THREAD * 2, map.size());
    }

    @ThreadSafe
    public static class ThreadSafeMap<K, V> extends ConcurrentHashMap<K, V> {
        @Override
        public void putAll(Map<? extends K, ? extends V> m) {
            synchronized (this) {
                super.putAll(m);
            }
        }

        @Override
        public V computeIfAbsent(K key, Function<? super K, ? extends V> mappingFunction) {
            synchronized (this) {
                return super.computeIfAbsent(key, mappingFunction);
            }
        }

        @Override
        public void replaceAll(BiFunction<? super K, ? super V, ? extends V> function) {
            synchronized (this) {
                super.replaceAll(function);
            }
        }
    }
}