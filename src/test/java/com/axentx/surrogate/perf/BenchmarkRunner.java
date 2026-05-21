package com.axentx.surrogate.perf;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import org.openjdk.jmh.annotations.*;

@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
public class BenchmarkRunner {

    private static final int SIZE = 100000;
    private List<Integer> arrayList;
    private List<Integer> copyOnWriteArrayList;
    private Map<Integer, Integer> concurrentHashMap;

    @Setup
    public void setup() {
        arrayList = new ArrayList<>();
        copyOnWriteArrayList = new CopyOnWriteArrayList<>();
        concurrentHashMap = new ConcurrentHashMap<>();
        for (int i = 0; i < SIZE; i++) {
            arrayList.add(i);
            copyOnWriteArrayList.add(i);
            concurrentHashMap.put(i, i);
        }
    }

    @Benchmark
    public void testArrayListRead() {
        for (int i = 0; i < SIZE; i++) {
            arrayList.get(i);
        }
    }

    @Benchmark
    public void testArrayListWrite() {
        for (int i = 0; i < SIZE; i++) {
            arrayList.set(i, i);
        }
    }

    @Benchmark
    public void testCopyOnWriteArrayListRead() {
        for (int i = 0; i < SIZE; i++) {
            copyOnWriteArrayList.get(i);
        }
    }

    @Benchmark
    public void testCopyOnWriteArrayListWrite() {
        for (int i = 0; i < SIZE; i++) {
            copyOnWriteArrayList.set(i, i);
        }
    }

    @Benchmark
    public void testConcurrentHashMapRead() {
        for (int i = 0; i < SIZE; i++) {
            concurrentHashMap.get(i);
        }
    }

    @Benchmark
    public void testConcurrentHashMapWrite() {
        for (int i = 0; i < SIZE; i++) {
            concurrentHashMap.put(i, i);
        }
    }
}

// src/main/java/com/axentx/surrogate/perf/PerformanceAnalyzer.java
package com.axentx.surrogate.perf;

import org.openjdk.jmh.results.RunResult;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.List;
import java.util.stream.Collectors;

public class PerformanceAnalyzer {

    public static void main(String[] args) throws Exception {
        Options opt = new OptionsBuilder()
                .include(BenchmarkRunner.class.getSimpleName())
                .forks(1)
                .build();

        List<RunResult> runResults = new Runner(opt).run();
        
        System.out.println("Benchmark Results:");
        for (RunResult result : runResults) {
            System.out.println("Benchmark: " + result.getBenchmark());
            System.out.println("Score: " + result.getPrimaryResult().getScore());
            System.out.println("Error: " + result.getPrimaryResult().getScoreError());
            System.out.println("Unit: " + result.getPrimaryResult().getScoreUnit());
            System.out.println("Parameters: " + result.getParams());
            System.out.println();
        }

        generateRefactoringSuggestions(runResults);
    }

    private static void generateRefactoringSuggestions(List<RunResult> runResults) {
        // Analyze results and provide actionable refactoring suggestions
        String suggestions = runResults.stream()
                .map(result -> "Consider using " + result.getBenchmark() + " for better performance with score: " 
                        + result.getPrimaryResult().getScore() + " " + result.getPrimaryResult().getScoreUnit() + ".")
                .collect(Collectors.joining("\n"));
        System.out.println("Refactoring Suggestions:\n" + suggestions);
    }
}