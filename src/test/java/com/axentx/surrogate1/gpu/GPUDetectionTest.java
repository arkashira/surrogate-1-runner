import org.junit.Test;
import static org.junit.Assert.*;

public class GPUDetectionTest {

    @Test
    public void testGPUDetection() {
        // Initialize the GPU detector
        GPUDetector detector = new GPUDetector();

        // Simulate multiple GPUs
        detector.addGPU("GPU1");
        detector.addGPU("GPU2");
        detector.addGPU("GPU3");

        // Test if the detector can detect multiple GPUs
        assertTrue(detector.getGPUs().size() == 3);
    }

    @Test
    public void testGPUConfiguration() {
        // Initialize the GPU detector
        GPUDetector detector = new GPUDetector();

        // Simulate multiple GPUs
        detector.addGPU("GPU1");
        detector.addGPU("GPU2");
        detector.addGPU("GPU3");

        // Test if the detector can configure GPUs for optimal load-balancing
        detector.configureGPUs();
        assertTrue(detector.getGPUs().get(0).isConfigured());
        assertTrue(detector.getGPUs().get(1).isConfigured());
        assertTrue(detector.getGPUs().get(2).isConfigured());
    }

    @Test
    public void testGamingPerformance() {
        // Initialize the GPU detector
        GPUDetector detector = new GPUDetector();

        // Simulate multiple GPUs
        detector.addGPU("GPU1");
        detector.addGPU("GPU2");
        detector.addGPU("GPU3");

        // Test if the detector can improve gaming performance by at least 2x bandwidth
        detector.configureGPUs();
        double bandwidth = detector.getBandwidth();
        assertTrue(bandwidth >= 2 * detector.getBaseBandwidth());
    }
}