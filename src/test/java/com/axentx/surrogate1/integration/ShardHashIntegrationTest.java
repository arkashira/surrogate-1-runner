package com.axentx.surrogate1.integration;

import com.axentx.surrogate1.shard.ShardHash;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
@ActiveProfiles("test")
public class ShardHashIntegrationTest {

    @Autowired
    private ShardHash shardHash;

    @Test
    public void testShardHashProcess() {
        // Test the shard hash process
        boolean result = shardHash.process();
        assertTrue(result, "Shard hash process should complete successfully");
    }

    @Test
    public void testShardHashStream() {
        // Test the shard hash stream functionality
        boolean result = shardHash.stream();
        assertTrue(result, "Shard hash stream should complete successfully");
    }

    @Test
    public void testShardHashNormalize() {
        // Test the shard hash normalize functionality
        boolean result = shardHash.normalize();
        assertTrue(result, "Shard hash normalize should complete successfully");
    }

    @Test
    public void testShardHashDedup() {
        // Test the shard hash dedup functionality
        boolean result = shardHash.dedup();
        assertTrue(result, "Shard hash dedup should complete successfully");
    }

    @Test
    public void testShardHashUpload() {
        // Test the shard hash upload functionality
        boolean result = shardHash.upload();
        assertTrue(result, "Shard hash upload should complete successfully");
    }
}