package com.axentx.gpu;

/**
 * Utility class for calculating and optimizing GPU bandwidth usage.
 *
 * <p>The calculations assume 32‑bit (4 byte) color depth per pixel.
 * Compression ratios are expressed as a fraction of the raw bandwidth
 * (e.g. 0.1 means 10% of raw bandwidth).
 *
 * <p>All bandwidth values are returned in gigabytes per second (GB/s).
 */
public final class BandwidthOptimizer {

    private static final int BYTES_PER_PIXEL = 4; // 32‑bit color depth

    private BandwidthOptimizer() {
        // Utility class; prevent instantiation
    }

    /**
     * Calculates the raw bandwidth required for a given resolution and frame rate.
     *
     * @param width  horizontal resolution in pixels
     * @param height vertical resolution in pixels
     * @param fps    frames per second
     * @return raw bandwidth in GB/s
     */
    public static double calculateRawBandwidth(int width, int height, int fps) {
        long pixelsPerFrame = (long) width * height;
        long bytesPerFrame = pixelsPerFrame * BYTES_PER_PIXEL;
        long bytesPerSecond = bytesPerFrame * fps;
        return bytesPerSecond / 1_000_000_000.0; // convert to GB/s
    }

    /**
     * Calculates the effective bandwidth after applying a compression ratio.
     *
     * @param rawBandwidth raw bandwidth in GB/s
     * @param compressionRatio compression ratio (0 < ratio <= 1)
     * @return effective bandwidth in GB/s
     */
    public static double calculateEffectiveBandwidth(double rawBandwidth, double compressionRatio) {
        if (compressionRatio <= 0 || compressionRatio > 1) {
            throw new IllegalArgumentException("Compression ratio must be in (0, 1]");
        }
        return rawBandwidth * compressionRatio;
    }

    /**
     * Determines the compression ratio required to keep bandwidth usage
     * below or equal to the specified target bandwidth.
     *
     * @param targetBandwidthGBps desired maximum bandwidth in GB/s
     * @param width  resolution width
     * @param height resolution height
     * @param fps    frame rate
     * @return compression ratio needed (0 < ratio <= 1)
     */
    public static double optimizeCompression(double targetBandwidthGBps, int width, int height, int fps) {
        double raw = calculateRawBandwidth(width, height, fps);
        if (raw <= targetBandwidthGBps) {
            // No compression needed; return 1.0 (100% of raw)
            return 1.0;
        }
        double ratio = targetBandwidthGBps / raw;
        // Clamp to [0,1] just in case
        if (ratio < 0) {
            return 0.0;
        }
        return Math.min(ratio, 1.0);
    }

    /**
     * Example usage: prints the bandwidth for 4K @ 60fps with 10% compression.
     */
    public static void main(String[] args) {
        int width = 3840;
        int height = 2160;
        int fps = 60;
        double compression = 0.10; // 10% of raw

        double raw = calculateRawBandwidth(width, height, fps);
        double effective = calculateEffectiveBandwidth(raw, compression);

        System.out.printf("Raw bandwidth: %.3f GB/s%n", raw);
        System.out.printf("Effective bandwidth (%.0f%% compression): %.3f GB/s%n",
                compression * 100, effective);
    }
}