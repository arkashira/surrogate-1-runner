package com.axentx.surrogate.gpu;

import java.util.ArrayList;
import java.util.List;

public class GPUDetector {
    public List<GPU> detectGPUs() {
        List<GPU> gpus = new ArrayList<>();
        // Simulate GPU detection logic
        // In a real implementation, this would interface with the system's GPU drivers
        gpus.add(new GPU("GPU-0", "NVIDIA", "RTX 3080", 8192));
        gpus.add(new GPU("GPU-1", "AMD", "RX 6800", 16384));
        return gpus;
    }
}