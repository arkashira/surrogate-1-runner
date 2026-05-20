package com.axentx.gpu;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BandwidthOptimizerTest {

    @Test
    void testCalculateRawBandwidth4K60fps() {
        double raw = BandwidthOptimizer.calculateRawBandwidth(3840, 2160, 60);
        // 3840*2160*4 bytes/frame = 33,177,600 bytes/frame
        // 33,177,600 * 60 = 1,990,656,000 bytes/s ≈ 1.991 GB/s
        assertEquals(1.991, raw, 0.001);
    }

    @Test
    void testCalculateEffectiveBandwidthWithCompression() {
        double raw = BandwidthOptimizer.calculateRawBandwidth(3840, 2160, 60);
        double effective = BandwidthOptimizer.calculateEffectiveBandwidth(raw, 0.10);
        // 10% of 1.991 GB/s ≈ 0.199 GB/s
        assertEquals(0.199, effective, 0.001);
    }

    @Test
    void testOptimizeCompressionBelowTarget() {
        double target = 100.0; // GB/s
        double ratio = BandwidthOptimizer.optimizeCompression(target, 3840, 2160, 60);
        // Raw bandwidth is ~1.991 GB/s, so no compression needed
        assertEquals(1.0, ratio, 0.0001);
    }

    @Test
    void testOptimizeCompressionAboveTarget() {
        double target = 0.5; // GB/s
        double ratio = BandwidthOptimizer.optimizeCompression(target, 3840, 2160, 60);
        // Raw bandwidth ~1.991 GB/s, ratio = 0.5 / 1.991 ≈ 0.251
        assertEquals(0.251, ratio, 0.001);
    }

    @Test
    void testCompressionRatioBounds() {
        assertThrows(IllegalArgumentException.class,
                () -> BandwidthOptimizer.calculateEffectiveBandwidth(1.0, 0.0));
        assertThrows(IllegalArgumentException.class,
                () -> BandwidthOptimizer.calculateEffectiveBandwidth(1.0, -0.1));
        assertThrows(IllegalArgumentException.class,
                () -> BandwidthOptimizer.calculateEffectiveBandwidth(1.0, 1.1));
    }
}