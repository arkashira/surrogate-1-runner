package com.axentx.surrogate1.renderer;

public class GamingGpuRenderer {
    private int gpuCount;

    public GamingGpuRenderer(int gpuCount) {
        if (gpuCount < 2) {
            throw new IllegalArgumentException("GPU count must be greater than 2");
        }
        this.gpuCount = gpuCount;
    }

    public int getGpuCount() {
        return gpuCount;
    }

    public float renderFrame(int width, int height) {
        // Simulate rendering a frame with multiple GPUs
        float baseFps = 60.0f * gpuCount;
        if (width >= 4096 && height >= 2160) { // 4K resolution
            return baseFps * 2;
        } else if (width >= 7680 && height >= 4320) { // 8K resolution
            return baseFps * 1.5f;
        }
        return baseFps;
    }
}