package com.example.cloudopt;

public final class VirtualMachine implements CloudResource {
    private final String id;
    private final String size;          // e.g. "large", "medium"
    private final double cpuUtil;       // 0.0 – 1.0
    private final double memUtil;       // 0.0 – 1.0

    public VirtualMachine(String id, String size, double cpuUtil, double memUtil) {
        this.id = id; this.size = size; this.cpuUtil = cpuUtil; this.memUtil = memUtil;
    }

    public String getId() { return id; }
    public String getSize() { return size; }
    public double getCpuUtilization() { return cpuUtil; }
    public double getMemoryUtilization() { return memUtil; }

    /** Very naive suggestion – replace “large” with “medium”. */
    public String getSuggestedSize() {
        return size.replace("large", "medium");
    }

    /** Placeholder for the real API call. */
    public void downsize() { /* … */ }
}