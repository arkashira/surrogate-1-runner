package com.axentx.surrogate.gpu;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.List;

public class MultiGPURendererTest {
    @Test
    public void testMultiGPURendererWithLessThanTwoGPUs() {
        List<GPU> gpus = Arrays.asList(new GPU());
        assertThrows(IllegalArgumentException.class, () -> new MultiGPURenderer(gpus));
    }

    @Test
    public void testMultiGPURendererWithTwoGPUs() {
        List<GPU> gpus = Arrays.asList(new GPU(), new GPU());
        assertDoesNotThrow(() -> new MultiGPURenderer(gpus));
    }

    @Test
    public void testRender() {
        List<GPU> gpus = Arrays.asList(new GPU(), new GPU());
        MultiGPURenderer renderer = new MultiGPURenderer(gpus);
        assertDoesNotThrow(() -> renderer.render(new Scene()));
    }

    @Test
    public void testSetResolution() {
        List<GPU> gpus = Arrays.asList(new GPU(), new GPU());
        MultiGPURenderer renderer = new MultiGPURenderer(gpus);
        assertDoesNotThrow(() -> renderer.setResolution(3840, 2160));
    }

    @Test
    public void testSetFrameRate() {
        List<GPU> gpus = Arrays.asList(new GPU(), new GPU());
        MultiGPURenderer renderer = new MultiGPURenderer(gpus);
        assertDoesNotThrow(() -> renderer.setFrameRate(120));
    }
}