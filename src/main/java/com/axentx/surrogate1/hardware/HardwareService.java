package com.axentx.surrogate1.hardware;

public class HardwareService {

    public static void main(String[] args) {
        // Detect hardware configuration
        String hardwareInfo = HardwareDetector.detectHardwareConfiguration();
        System.out.println("Hardware Configuration:\n" + hardwareInfo);

        // Profile hardware performance
        String performanceInfo = HardwareProfiler.profileHardwarePerformance();
        System.out.println("Hardware Performance:\n" + performanceInfo);

        // Optimize hardware configuration
        String recommendations = HardwareOptimizer.optimizeHardwareConfiguration(hardwareInfo, performanceInfo);
        System.out.println("Optimization Recommendations:\n" + recommendations);
    }
}