package com.axentx.surrogate.gpu;

import java.util.List;

public class MultiGPURenderer {
    private List<GPU> gpus;

    public MultiGPURenderer(List<GPU> gpus) {
        if (gpus.size() < 2) {
            throw new IllegalArgumentException("At least two GPUs are required for multi-GPU rendering.");
        }
        this.gpus = gpus;
    }

    public void render(Scene scene) {
        // Distribute the rendering workload across multiple GPUs
        for (GPU gpu : gpus) {
            gpu.render(scene);
        }
    }

    public void setResolution(int width, int height) {
        // Set the resolution for all GPUs
        for (GPU gpu : gpus) {
            gpu.setResolution(width, height);
        }
    }

    public void setFrameRate(int fps) {
        // Set the frame rate for all GPUs
        for (GPU gpu : gpus) {
            gpu.setFrameRate(fps);
        }
    }
}