package com.axentx.surrogate.gpu;

import java.util.List;

public class GPUManager {
    private GPUDetector gpuDetector;
    private GPUConfigurator gpuConfigurator;

    public GPUManager() {
        this.gpuDetector = new GPUDetector();
        this.gpuConfigurator = new GPUConfigurator();
    }

    public void manageGPUs() {
        List<GPU> gpus = gpuDetector.detectGPUs();
        gpuConfigurator.configureGPUs(gpus);
    }
}