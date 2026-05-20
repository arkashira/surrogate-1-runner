package com.axentx.surrogate.dataset;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class DatasetLoader {

    private static final int NUM_THREADS = 16;
    private static final String DATASET_PATH = "/path/to/dataset";

    public void loadDataset() throws IOException {
        ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);

        IntStream.range(0, NUM_THREADS).forEach(shardId -> {
            executor.submit(() -> {
                try {
                    loadShard(shardId);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
        });

        executor.shutdown();
    }

    private void loadShard(int shardId) throws IOException {
        String shardPath = DATASET_PATH + "/shard_" + shardId;
        byte[] shardData = Files.readAllBytes(Paths.get(shardPath));
        // Process shard data
    }
}