package com.axentx.surrogate1;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermission;
import java.time.Instant;
import java.util.EnumSet;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * A simple service that records a radio stream by writing dummy data to a file.
 * <p>
 * In a real implementation this would connect to the stream URL and pipe the
 * audio data to the file. For the purposes of the tests we simulate the
 * recording by writing timestamped bytes until stopped.
 * </p>
 */
public class RecordingService {

    private Path recordingPath;
    private String streamUrl;
    private final AtomicBoolean recording = new AtomicBoolean(false);
    private Thread recordingThread;

    /**
     * Starts recording the given stream URL.
     *
     * @param streamUrl the URL of the radio stream to record
     * @throws IllegalStateException if a recording is already in progress
     * @throws IOException           if the recording file cannot be created
     */
    public synchronized void startRecording(String streamUrl) throws IOException {
        if (recording.get()) {
            throw new IllegalStateException("Recording already in progress");
        }
        this.streamUrl = streamUrl;
        Path tempDir = Files.createTempDirectory("radio_recording");
        recordingPath = tempDir.resolve("recording_" + Instant.now().toEpochMilli() + ".mp3");
        // Secure the file: owner read/write only
        try {
            Set<PosixFilePermission> perms = EnumSet.of(PosixFilePermission.OWNER_READ,
                    PosixFilePermission.OWNER_WRITE);
            Files.setPosixFilePermissions(recordingPath, perms);
        } catch (UnsupportedOperationException e) {
            // Windows does not support Posix permissions; ignore
        }

        recording.set(true);
        recordingThread = new Thread(this::recordLoop, "RadioRecordingThread");
        recordingThread.start();
    }

    /**
     * Stops the current recording.
     *
     * @throws IllegalStateException if no recording is in progress
     */
    public synchronized void stopRecording() {
        if (!recording.get()) {
            throw new IllegalStateException("No recording in progress");
        }
        recording.set(false);
        try {
            recordingThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Returns the path to the recording file.
     *
     * @return the recording file path, or null if no recording has been started
     */
    public Path getRecordingPath() {
        return recordingPath;
    }

    /**
     * Returns the URL of the stream currently being recorded.
     *
     * @return the stream URL, or null if no recording has been started
     */
    public String getStreamUrl() {
        return streamUrl;
    }

    /**
     * Returns true if a recording is in progress.
     *
     * @return true if recording, false otherwise
     */
    public boolean isRecording() {
        return recording.get();
    }

    /**
     * The main loop that writes dummy data to the recording file until stopped.
     */
    private void recordLoop() {
        try (OutputStream out = Files.newOutputStream(recordingPath,
                StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {
            while (recording.get()) {
                byte[] data = ("Timestamp: " + Instant.now() + "\n").getBytes();
                out.write(data);
                out.flush();
                Thread.sleep(500); // simulate 0.5s of data
            }
        } catch (IOException | InterruptedException e) {
            // In a real implementation we would log this
            Thread.currentThread().interrupt();
        }
    }
}