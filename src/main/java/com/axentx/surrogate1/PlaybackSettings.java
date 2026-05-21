package com.axentx.surrogate1;

/**
 * Holds playback configuration that can be tuned at runtime based on system resources.
 * 
 * <p>Provides three tiers of quality settings suitable for different device capabilities:
 * <ul>
 *   <li>Low-end: 480p, 1500 kbps, 5000ms buffer</li>
 *   <li>Mid-range: 720p, 3000 kbps, 4000ms buffer</li>
 *   <li>High-end: 1080p, 5000 kbps, 3000ms buffer</li>
 * </ul>
 */
public class PlaybackSettings {

    private int resolutionHeight;
    private int bitrateKbps;
    private int bufferMs;

    public PlaybackSettings() {
        // Default to high-end settings
        this.resolutionHeight = 1080;
        this.bitrateKbps = 5000;
        this.bufferMs = 3000;
    }

    // Getters
    public int getResolutionHeight() { return resolutionHeight; }
    public int getBitrateKbps() { return bitrateKbps; }
    public int getBufferMs() { return bufferMs; }

    // Setters
    public void setResolutionHeight(int resolutionHeight) { this.resolutionHeight = resolutionHeight; }
    public void setBitrateKbps(int bitrateKbps) { this.bitrateKbps = bitrateKbps; }
    public void setBufferMs(int bufferMs) { this.bufferMs = bufferMs; }

    /**
     * Adjusts settings based on available heap memory.
     * 
     * @param freeHeapMiB Available free heap in megabytes
     */
    public void adjust(long freeHeapMiB) {
        if (freeHeapMiB < 100) {
            // Low-end device: reduce all metrics
            this.resolutionHeight = 480;
            this.bitrateKbps = 1500;
            this.bufferMs = 5000;
        } else if (freeHeapMiB < 300) {
            // Mid-range device: balanced settings
            this.resolutionHeight = 720;
            this.bitrateKbps = 3000;
            this.bufferMs = 4000;
        } else {
            // High-end device: maximum quality
            this.resolutionHeight = 1080;
            this.bitrateKbps = 5000;
            this.bufferMs = 3000;
        }
    }

    @Override
    public String toString() {
        return String.format("PlaybackSettings{resolution=%dp, bitrate=%dkbps, buffer=%dms}",
                resolutionHeight, bitrateKbps, bufferMs);
    }
}