package com.axentx.surrogate1.test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import com.axentx.surrogate1.worker.GamingGpuWorker;

class GamingGpuWorkerTest {

    @Test
    void testGpuAvailability() {
        GamingGpuWorker worker = new GamingGpuWorker();
        assertTrue(worker.isGpuAvailable(), "Gaming GPU should be available");
    }

    @Test
    void testGpuProcessing() {
        GamingGpuWorker worker = new GamingGpuWorker();
        String testData = "test graphics data";
        String processedData = worker.processWithGpu(testData);
        assertNotNull(processedData, "Processed data should not be null");
        assertFalse(processedData.equals(testData), "Processed data should be different from input");
    }
}