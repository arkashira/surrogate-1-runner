
package com.axentx.rendering;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
public class RenderingLatencyTest {

    private static final int WIDTH = 1920;
    private static final int HEIGHT = 1080;

    @Param({"low", "medium", "high"})
    private String scene;

    private Blackhole blackhole;

    @Setup
    public void setup() {
        // Initialize rendering engine
        // ...

        blackhole = new Blackhole();
    }

    @Benchmark
    public void render() {
        // Render scene
        // ...

        blackhole.consume(true); // Discard result to avoid caching
    }

    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(RenderingLatencyTest.class.getSimpleName())
                .warmupIterations(5)
                .measurementIterations(5)
                .forks(1)
                .build();

        new Runner(opt).run();
    }
}