package com.axentx.surrogate1;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;

/**
 * Central manager that creates and updates PlaybackSettings based on system resources.
 * 
 * <p>Provides both static utility methods and instance-based refresh capabilities.
 * Can be called periodically to adapt to changing system conditions.
 */
public class SettingsManager {

    private final PlaybackSettings playbackSettings;
    private final MemoryMXBean memoryMXBean;

    public SettingsManager() {
        this.playbackSettings = new PlaybackSettings();
        this.memoryMXBean = ManagementFactory.getMemoryMXBean();
    }

    public PlaybackSettings getPlaybackSettings() {
        return playbackSettings;
    }

    /**
     * Refreshes settings based on current JVM memory statistics.
     * Lightweight enough to call periodically (e.g., every few seconds).
     */
    public void refreshSettings() {
        SystemResources resources = captureSystemResources();
        playbackSettings.adjust(resources.getFreeHeapMiB());
    }

    /**
     * Captures current JVM heap memory usage.
     */
    private SystemResources captureSystemResources() {
        MemoryMXBean mxBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heap = mxBean.getHeapMemoryUsage();
        return new SystemResources(
            heap.getFree(),
            heap.getUsed(),
            heap.getMax()
        );
    }

    // Static convenience method (from Candidate 1's approach)
    public static PlaybackSettings adjustPlaybackSettings() {
        SettingsManager manager = new SettingsManager();
        manager.refreshSettings();
        return manager.getPlaybackSettings();
    }
}