package com.axentx.surrogate1.service;

import java.util.*;
import java.io.File;
import java.nio.file.*;

public class WorkerDiscoverer {
    
    private static final String WORKER_DIR_PATH = "/opt/axentx/surrogate-1/workers";
    private static final String WORKER_PATTERN = "worker-*.jar";
    
    /**
     * Discovers existing Surrogate-1 ingest workers by scanning the worker directory
     * @return List of discovered worker paths
     */
    public List<String> discoverWorkers() {
        List<String> workers = new ArrayList<>();
        
        try {
            Path workerDir = Paths.get(WORKER_DIR_PATH);
            
            // Check if directory exists
            if (!Files.exists(workerDir)) {
                return workers;
            }
            
            // Scan for worker JAR files
            Files.walkFileTree(workerDir, new SimpleFileVisitor<Path>() {
                @Override
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                    if (file.toString().matches(".*" + WORKER_PATTERN.replace("*", ".*"))) {
                        workers.add(file.toString());
                    }
                    return FileVisitResult.CONTINUE;
                }
            });
            
        } catch (Exception e) {
            // Log error but don't fail completely
            System.err.println("Error discovering workers: " + e.getMessage());
        }
        
        return workers;
    }
    
    /**
     * Gets detailed information about a specific worker
     * @param workerPath Path to the worker JAR
     * @return WorkerInfo object with details
     */
    public WorkerInfo getWorkerInfo(String workerPath) {
        WorkerInfo info = new WorkerInfo();
        info.setPath(workerPath);
        
        try {
            Path path = Paths.get(workerPath);
            info.setName(path.getFileName().toString());
            info.setLastModified(Files.getLastModifiedTime(path));
            info.setSize(Files.size(path));
            
            // Extract worker type from filename pattern
            String fileName = path.getFileName().toString();
            if (fileName.startsWith("worker-") && fileName.endsWith(".jar")) {
                String[] parts = fileName.substring(7, fileName.length() - 4).split("-");
                if (parts.length > 0) {
                    info.setType(parts[0]);
                }
            }
            
        } catch (Exception e) {
            System.err.println("Error getting worker info: " + e.getMessage());
        }
        
        return info;
    }
    
    /**
     * Represents information about a discovered worker
     */
    public static class WorkerInfo {
        private String path;
        private String name;
        private String type;
        private java.time.Instant lastModified;
        private long size;
        
        // Getters and setters
        public String getPath() { return path; }
        public void setPath(String path) { this.path = path; }
        
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        
        public String getType() { return type; }
        public void setType(String type) { this.type = type; }
        
        public java.time.Instant getLastModified() { return lastModified; }
        public void setLastModified(java.time.Instant lastModified) { this.lastModified = lastModified; }
        
        public long getSize() { return size; }
        public void setSize(long size) { this.size = size; }
    }
}