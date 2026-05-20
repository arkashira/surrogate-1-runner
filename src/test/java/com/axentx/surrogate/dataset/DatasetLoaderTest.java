package com.axentx.surrogate.dataset;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DatasetLoaderTest {

    @Test
    public void testLoadDataset() {
        DatasetLoader loader = new DatasetLoader();
        assertDoesNotThrow(() -> loader.loadDataset());
    }
}