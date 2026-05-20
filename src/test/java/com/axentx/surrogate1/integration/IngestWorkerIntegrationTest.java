package com.axentx.surrogate1.integration;

import com.axentx.surrogate1.worker.IngestWorker;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
@ActiveProfiles("test")
public class IngestWorkerIntegrationTest {

    @Autowired
    private IngestWorker ingestWorker;

    @Test
    public void testIngestWorkerProcess() {
        // Test the ingest worker process
        boolean result = ingestWorker.process();
        assertTrue(result, "Ingest worker process should complete successfully");
    }

    @Test
    public void testIngestWorkerStream() {
        // Test the ingest worker stream functionality
        boolean result = ingestWorker.stream();
        assertTrue(result, "Ingest worker stream should complete successfully");
    }

    @Test
    public void testIngestWorkerNormalize() {
        // Test the ingest worker normalize functionality
        boolean result = ingestWorker.normalize();
        assertTrue(result, "Ingest worker normalize should complete successfully");
    }

    @Test
    public void testIngestWorkerDedup() {
        // Test the ingest worker dedup functionality
        boolean result = ingestWorker.dedup();
        assertTrue(result, "Ingest worker dedup should complete successfully");
    }

    @Test
    public void testIngestWorkerUpload() {
        // Test the ingest worker upload functionality
        boolean result = ingestWorker.upload();
        assertTrue(result, "Ingest worker upload should complete successfully");
    }
}