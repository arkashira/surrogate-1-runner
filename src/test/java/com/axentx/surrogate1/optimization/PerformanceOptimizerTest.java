package com.axentx.surrogate1.optimization;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for {@link PerformanceOptimizer} ensuring that dynamic GPU adjustments
 * are applied correctly across a range of game scenarios while preserving
 * system stability.
 */
class PerformanceOptimizerTest {

    private PerformanceOptimizer optimizer;

    @BeforeEach
    void setUp() {
        optimizer = new PerformanceOptimizer();
    }

    /**
     * Simulates a low‑resolution indie title. The optimizer should keep the GPU
     * clocks modest while guaranteeing stability.
     */
    @Test
    void testLowResolutionGameAdjustment() {
        GameScenario scenario = new GameScenario("IndieGame", 1280, 720);
        OptimizationResult result = optimizer.optimize(scenario);

        assertTrue(result.isStable(), "System must remain stable for low‑resolution games");
        assertTrue(
                result.getGpuClockMHz() >= 1000 && result.getGpuClockMHz() <= 1500,
                "GPU clock should be within the low‑performance range"
        );
    }

    /**
     * Simulates a high‑resolution AAA title. The optimizer should boost GPU
     * clocks appropriately while still keeping the system stable.
     */
    @Test
    void testHighResolutionGameAdjustment() {
        GameScenario scenario = new GameScenario("AAA_Title", 3840, 2160);
        OptimizationResult result = optimizer.optimize(scenario);

        assertTrue(result.isStable(), "System must remain stable for high‑resolution games");
        assertTrue(
                result.getGpuClockMHz() >= 1500 && result.getGpuClockMHz() <= 2000,
                "GPU clock should be within the high‑performance range"
        );
    }

    /**
     * Rapidly switches between several game scenarios to verify that each
     * dynamic adjustment maintains stability.
     */
    @Test
    void testDynamicAdjustmentStability() {
        GameScenario[] scenarios = {
                new GameScenario("GameA", 1920, 1080),
                new GameScenario("GameB", 2560, 1440),
                new GameScenario("GameC", 1280, 720)
        };

        for (GameScenario scenario : scenarios) {
            OptimizationResult result = optimizer.optimize(scenario);
            assertTrue(result.isStable(),
                    "Dynamic adjustment for " + scenario.getGameName() + " must keep the system stable");
        }
    }
}