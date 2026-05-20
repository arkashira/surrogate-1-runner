package com.axentx.surrogate1.collections;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
@Fork(value = 1, jvmArgs = {"-Xms2G", "-Xmx2G"})
public class SynchronizedCollectionsBenchmarkTest {

    private static final int MAP_SIZE = 1000000;

    private Map<Integer, Integer> synchronizedMap;
    private Map<Integer, Integer> concurrentMap;

    @Setup
    public void setup() {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < MAP_SIZE; i++) {
            map.put(i, i);
        }
        synchronizedMap = Collections.synchronizedMap(map);
        concurrentMap = new java.util.concurrent.ConcurrentHashMap<>(map);
    }

    @Benchmark
    public void testSynchronizedMapPut() {
        synchronizedMap.put(MAP_SIZE, MAP_SIZE);
    }

    @Benchmark
    public void testConcurrentMapPut() {
        concurrentMap.put(MAP_SIZE, MAP_SIZE);
    }

    @Benchmark
    public void testSynchronizedMapGet() {
        synchronizedMap.get(MAP_SIZE / 2);
    }

    @Benchmark
    public void testConcurrentMapGet() {
        concurrentMap.get(MAP_SIZE / 2);
    }

    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(SynchronizedCollectionsBenchmarkTest.class.getSimpleName())
                .build();

        new Runner(opt).run();
    }
}