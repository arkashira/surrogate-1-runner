package com.axentx.surrogate.dataset;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DatasetShardTest {

    @Test
    public void testDatasetShard() {
        int shardId = 1;
        byte[] data = new byte[]{1, 2, 3};
        DatasetShard shard = new DatasetShard(shardId, data);

        assertEquals(shardId, shard.getShardId());
        assertArrayEquals(data, shard.getData());
    }
}