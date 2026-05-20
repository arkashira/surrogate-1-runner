package com.axentx.surrogate;

import java.io.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class IngestionService {
    private static final int DEFAULT_THREAD_POOL_SIZE = Runtime.getRuntime().availableProcessors();
    private static final int BATCH_SIZE = 100;
    private static final int MAX_RETRIES = 3;
    private final ExecutorService executorService;
    private final Path dataStorePath;
    private final Path outputPath;
    private final Phaser phaser;

    public IngestionService(Path dataStorePath, Path outputPath) {
        this(dataStorePath, outputPath, DEFAULT_THREAD_POOL_SIZE);
    }

    public IngestionService(Path dataStorePath, Path outputPath, int threadPoolSize) {
        this.dataStorePath = dataStorePath;
        this.outputPath = outputPath;
        this.executorService = Executors.newWorkStealingPool(threadPoolSize);
        this.phaser = new Phaser(1); // Register main thread
    }

    public IngestionResult ingest(List<String> datasetUrls) throws IOException, InterruptedException {
        long startTime = System.currentTimeMillis();

        // Process in parallel using work-stealing pool
        List<CompletableFuture<IngestionChunkResult>> futures = datasetUrls.stream()
            .collect(Collectors.groupingBy(url -> Math.abs(url.hashCode()) % BATCH_SIZE))
            .values().stream()
            .map(chunk -> CompletableFuture.supplyAsync(() -> processChunk(chunk), executorService))
            .collect(Collectors.toList());

        // Aggregate results
        List<IngestedRecord> allRecords = Collections.synchronizedList(new ArrayList<>());
        Set<String> allHashes = ConcurrentHashMap.newKeySet();
        int totalErrors = 0;

        for (CompletableFuture<IngestionChunkResult> future : futures) {
            try {
                IngestionChunkResult result = future.get();
                allRecords.addAll(result.getRecords());
                allHashes.addAll(result.getHashes());
                totalErrors += result.getErrorCount();
            } catch (ExecutionException e) {
                totalErrors++;
            }
        }

        long endTime = System.currentTimeMillis();

        // Write output asynchronously
        CompletableFuture.runAsync(() -> {
            try {
                writeOutput(allRecords);
            } catch (IOException e) {
                // Log error
            }
        }, executorService);

        return new IngestionResult(
            allRecords.size(),
            allHashes.size(),
            totalErrors,
            endTime - startTime
        );
    }

    private IngestionChunkResult processChunk(List<String> urls) {
        List<IngestedRecord> records = new ArrayList<>();
        Set<String> hashes = ConcurrentHashMap.newKeySet();
        int errorCount = 0;

        for (String url : urls) {
            int attempts = 0;
            boolean success = false;

            while (attempts < MAX_RETRIES && !success) {
                try {
                    IngestedRecord record = fetchAndProcess(url);
                    records.add(record);
                    hashes.add(record.getHash());
                    success = true;
                } catch (Exception e) {
                    attempts++;
                    if (attempts == MAX_RETRIES) {
                        errorCount++;
                    }
                }
            }
        }

        return new IngestionChunkResult(records, hashes, errorCount);
    }

    private IngestedRecord fetchAndProcess(String url) throws IOException {
        String data = fetchData(url);
        String normalized = normalizeData(data);
        String hash = computeHash(normalized);
        return new IngestedRecord(url, normalized, hash);
    }

    private String fetchData(String url) throws IOException {
        // Implement actual HTTP fetch with timeout
        try (InputStream in = new URL(url).openStream()) {
            return new String(in.readAllBytes());
        }
    }

    private String normalizeData(String data) {
        return data.trim().toLowerCase().replaceAll("\\s+", " ");
    }

    private String computeHash(String data) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] digest = md.digest(data.getBytes());
            return Base64.getEncoder().encodeToString(digest);
        } catch (Exception e) {
            return UUID.randomUUID().toString();
        }
    }

    private void writeOutput(List<IngestedRecord> records) throws IOException {
        Files.createDirectories(outputPath.getParent());
        try (BufferedWriter writer = Files.newBufferedWriter(outputPath)) {
            for (IngestedRecord record : records) {
                writer.write(record.toJson());
                writer.newLine();
            }
        }
    }

    public void shutdown() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(60, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }

    // Inner classes remain the same as in the original
    // ...
}