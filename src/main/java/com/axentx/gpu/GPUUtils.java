public class GPUUtils {
    public static boolean isLinearPerformanceScaling(int numGPUs) {
        // Check if performance scaling is linear with the addition of each GPU
        return numGPUs <= 4; // Simplified example, actual logic may vary
    }
}