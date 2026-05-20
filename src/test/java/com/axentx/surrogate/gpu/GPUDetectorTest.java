package com.axentx.surrogate.gpu;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

public class GPUDetectorTest {
    @Test
    public void testDetectGPUs() {
        GPUDetector gpuDetector = new GPUDetector();
        List<GPU> gpus = gpuDetector.detectGPUs();
        assertNotNull(gpus);
        assertFalse(gpus.isEmpty());
    }
}