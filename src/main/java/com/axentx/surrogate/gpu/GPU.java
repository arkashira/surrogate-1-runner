package com.axentx.surrogate.gpu;

public class GPU {
    private int resolutionWidth;
    private int resolutionHeight;
    private int frameRate;

    public void render(Scene scene) {
        // Render the scene using the GPU
    }

    public void setResolution(int width, int height) {
        this.resolutionWidth = width;
        this.resolutionHeight = height;
    }

    public void setFrameRate(int fps) {
        this.frameRate = fps;
    }
}