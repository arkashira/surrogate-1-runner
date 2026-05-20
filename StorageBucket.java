package com.example.cloudopt;

public final class StorageBucket implements CloudResource {
    private final String id;
    private final long lastAccessedHoursAgo;

    public StorageBucket(String id, long lastAccessedHoursAgo) {
        this.id = id; this.lastAccessedHoursAgo = lastAccessedHoursAgo;
    }

    public String getId() { return id; }
    public long getLastAccessedHoursAgo() { return lastAccessedHoursAgo; }

    public void archive() { /* … */ }
}