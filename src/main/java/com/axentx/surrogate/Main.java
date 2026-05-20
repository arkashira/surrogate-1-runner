package com.axentx.surrogate;

import com.axentx.surrogate.gpu.GPUManager;

public class Main {
    public static void main(String[] args) {
        GPUManager gpuManager = new GPUManager();
        gpuManager.manageGPUs();
    }
}