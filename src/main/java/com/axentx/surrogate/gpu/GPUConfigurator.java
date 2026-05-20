package com.axentx.surrogate.gpu;

import java.util.List;

public class GPUConfigurator {
    public void configureGPUs(List<GPU> gpus) {
        // Simulate GPU configuration logic
        // In a real implementation, this would configure the GPUs for optimal load-balancing
        for (GPU gpu : gpus) {
            System.out.println("Configuring GPU: " + gpu.getId());
        }
    }
}