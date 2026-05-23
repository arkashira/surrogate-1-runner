package com.axentx.surrogate1;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Minimal media player simulation that uses {@link ResourceAllocator}
 * to adapt buffer size based on playback conditions.
 */
public class MediaPlayer {

    private final ResourceAllocator allocator;
    private final Timer timer = new Timer(true);
    private boolean isPlaying = false;

    public MediaPlayer() {
        this.allocator = new ResourceAllocator();
    }

    /**
     * Starts playback simulation.
     */
    public void play() {
        isPlaying = true;
        schedulePlaybackCheck();
    }

    /**
     * Stops playback simulation.
     */
    public void stop() {
        isPlaying = false;
        timer.cancel();
    }

    /**
     * Simulates a playback check that randomly decides if buffering
     * or smooth playback occurs. Adjusts the buffer size accordingly.
     */
    private void schedulePlaybackCheck() {
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                if (!isPlaying) {
                    return;
                }
                // Randomly simulate buffering or smooth playback
                boolean buffering = Math.random() < 0.2; // 20% chance
                if (buffering) {
                    allocator.onBuffering();
                    System.out.println("[MediaPlayer] Buffering detected. Buffer size: "
                            + allocator.getBufferSize() + " ms");
                } else {
                    allocator.onSmoothPlayback();
                    System.out.println("[MediaPlayer] Smooth playback. Buffer size: "
                            + allocator.getBufferSize() + " ms");
                }
            }
        }, 0, 1000); // check every second
    }

    /**
     * Returns the current buffer size in milliseconds.
     *
     * @return buffer size in ms
     */
    public int getCurrentBufferSize() {
        return allocator.getBufferSize();
    }
}