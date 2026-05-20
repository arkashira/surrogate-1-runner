package com.axentx.surrogate1;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

class RecordingServiceTest {

    private final RecordingService service = new RecordingService();

    @AfterEach
    void tearDown() throws IOException {
        if (service.isRecording()) {
            service.stopRecording();
        }
        Path path = service.getRecordingPath();
        if (path != null && Files.exists(path)) {
            Files.deleteIfExists(path);
            Files.deleteIfExists(path.getParent());
        }
    }

    @Test
    void testStartAndStopRecording() throws IOException, InterruptedException {
        String streamUrl = "http://example.com/stream";
        service.startRecording(streamUrl);
        assertTrue(service.isRecording(), "Recording should be in progress");
        assertEquals(streamUrl, service.getStreamUrl(), "Stream URL should match");

        // Let it record for a short time
        Thread.sleep(1200);

        service.stopRecording();
        assertFalse(service.isRecording(), "Recording should have stopped");

        Path recordingPath = service.getRecordingPath();
        assertNotNull(recordingPath, "Recording path should not be null");
        assertTrue(Files.exists(recordingPath), "Recording file should exist");
        assertTrue(Files.size(recordingPath) > 0, "Recording file should contain data");
    }

    @Test
    void testConcurrentStartThrows() throws IOException {
        service.startRecording("http://example.com/stream");
        assertThrows(IllegalStateException.class, () -> service.startRecording("http://example.com/other"));
        service.stopRecording();
    }

    @Test
    void testStopWithoutStartThrows() {
        assertThrows(IllegalStateException.class, () -> service.stopRecording());
    }
}