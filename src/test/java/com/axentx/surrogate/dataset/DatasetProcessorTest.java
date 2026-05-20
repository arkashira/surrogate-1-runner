package com.axentx.surrogate.dataset;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DatasetProcessorTest {

    @Test
    public void testProcessShard() {
        DatasetProcessor processor = new DatasetProcessor();
        DatasetShard shard = new DatasetShard(1, new byte[]{1, 2, 3});
        assertDoesNotThrow(() -> processor.processShard(shard));
    }
}