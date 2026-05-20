package com.axentx.surrogate1.collections;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
@Fork(value = 1, jvmArgs = {"-Xms2G", "-Xmx2G"})
public class ConcurrentCollectionsBenchmarkTest {

    private static final int MAP_SIZE = 1000000;

    private Map<Integer, Integer> concurrentMap;

    @Setup
    public void setup() {
        concurrentMap = new ConcurrentHashMap<>();
        for (int i = 0; i < MAP_SIZE; i++) {
            concurrentMap.put(i, i);
        }
    }

    @Benchmark
    public void testConcurrentMapPut() {
        concurrentMap.put(MAP_SIZE, MAP_SIZE);
    }

    @Benchmark
    public void testConcurrentMapGet() {
        concurrentMap.get(MAP_SIZE / 2);
    }

    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(ConcurrentCollectionsBenchmarkTest.class.getSimpleName())
                .build();

        new Runner(opt).run();
    }
}