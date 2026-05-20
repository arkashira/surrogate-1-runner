package com.axentx.surrogate.gpu;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;

public class GPUConfiguratorTest {
    @Test
    public void testConfigureGPUs() {
        GPUConfigurator gpuConfigurator = new GPUConfigurator();
        List<GPU> gpus = new ArrayList<>();
        gpus.add(new GPU("GPU-0", "NVIDIA", "RTX 3080", 8192));
        gpuConfigurator.configureGPUs(gpus);
        // Add assertions to verify the configuration
    }
}