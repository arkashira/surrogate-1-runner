package com.axentx.surrogate1.test;

import static org.junit.Assert.*;
import org.junit.Test;
import com.axentx.surrogate1.renderer.GamingGpuRenderer;

public class GamingGpuRendererTest {

    @Test
    public void testMultiGpuRenderingPerformance() {
        GamingGpuRenderer renderer = new GamingGpuRenderer(4); // Test with 4 GPUs
        float fps = renderer.renderFrame(4096, 2160); // Test 4K resolution
        assertTrue(fps > 120);

        fps = renderer.renderFrame(7680, 4320); // Test 8K resolution
        assertTrue(fps > 120);
    }

    @Test
    public void testGpuCount() {
        GamingGpuRenderer renderer = new GamingGpuRenderer(3);
        assertEquals(3, renderer.getGpuCount());

        renderer = new GamingGpuRenderer(4);
        assertEquals(4, renderer.getGpuCount());
    }
}