package com.axentx.surrogate.datamanagement;

import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

public class LargeDatasetLoaderTest {

    @Test
    public void testLoadDataset() {
        String testFilePath = "test_dataset.txt"; // Ensure this file exists in the test environment
        assertDoesNotThrow(() -> new LargeDatasetLoader().loadDataset(testFilePath));
    }
}