package com.example.cloudopt;

public final class DatabaseInstance implements CloudResource {
    private final String id;
    private final int connectionPoolSize;
    private final int maxConnections;

    public DatabaseInstance(String id, int connectionPoolSize, int maxConnections) {
        this.id = id; this.connectionPoolSize = connectionPoolSize; this.maxConnections = maxConnections;
    }

    public String getId() { return id; }
    public int getConnectionPoolSize() { return connectionPoolSize; }
    public int getMaxConnections() { return maxConnections; }

    public void throttleConnections() { /* … */ }
}