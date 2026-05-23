package com.axentx.surrogate1;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * Simple adaptive resource allocator that adjusts the allocated buffer size
 * based on current playback conditions. The allocator exposes a single
 * method {@link #getBufferSize()} which returns the current buffer size in
 * milliseconds. The buffer size is increased when the playback is smooth
 * and decreased when buffering is detected.
 */
public class ResourceAllocator {

    // Minimum and maximum buffer sizes in milliseconds
    private static final int MIN_BUFFER_MS = 2000;
    private static final int MAX_BUFFER_MS = 8000;

    // Target buffer size to aim for under normal conditions
    private static final int TARGET_BUFFER_MS = 5000;

    // Adjustment step in milliseconds
    private static final int STEP_MS = 500;

    // Current buffer size
    private final AtomicInteger currentBufferMs = new AtomicInteger(TARGET_BUFFER_MS);

    /**
     * Called by the MediaPlayer when a buffering event occurs.
     * Decreases the buffer size to free resources for smoother playback.
     */
    public void onBuffering() {
        int newSize = Math.max(MIN_BUFFER_MS, currentBufferMs.get() - STEP_MS);
        currentBufferMs.set(newSize);
    }

    /**
     * Called by the MediaPlayer when playback is smooth.
     * Increases the buffer size to prefetch more data and reduce future buffering.
     */
    public void onSmoothPlayback() {
        int newSize = Math.min(MAX_BUFFER_MS, currentBufferMs.get() + STEP_MS);
        currentBufferMs.set(newSize);
    }

    /**
     * Returns the current buffer size in milliseconds.
     *
     * @return buffer size in ms
     */
    public int getBufferSize() {
        return currentBufferMs.get();
    }
}