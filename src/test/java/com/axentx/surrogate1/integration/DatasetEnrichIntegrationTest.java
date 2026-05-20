package com.axentx.surrogate1.integration;

import com.axentx.surrogate1.dataset.DatasetEnrich;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
@ActiveProfiles("test")
public class DatasetEnrichIntegrationTest {

    @Autowired
    private DatasetEnrich datasetEnrich;

    @Test
    public void testDatasetEnrichProcess() {
        // Test the dataset enrich process
        boolean result = datasetEnrich.process();
        assertTrue(result, "Dataset enrich process should complete successfully");
    }

    @Test
    public void testDatasetEnrichStream() {
        // Test the dataset enrich stream functionality
        boolean result = datasetEnrich.stream();
        assertTrue(result, "Dataset enrich stream should complete successfully");
    }

    @Test
    public void testDatasetEnrichNormalize() {
        // Test the dataset enrich normalize functionality
        boolean result = datasetEnrich.normalize();
        assertTrue(result, "Dataset enrich normalize should complete successfully");
    }

    @Test
    public void testDatasetEnrichDedup() {
        // Test the dataset enrich dedup functionality
        boolean result = datasetEnrich.dedup();
        assertTrue(result, "Dataset enrich dedup should complete successfully");
    }

    @Test
    public void testDatasetEnrichUpload() {
        // Test the dataset enrich upload functionality
        boolean result = datasetEnrich.upload();
        assertTrue(result, "Dataset enrich upload should complete successfully");
    }
}