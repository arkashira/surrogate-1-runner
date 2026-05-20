package com.axentx.surrogate1;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.nio.file.*;

import static org.junit.jupiter.api.Assertions.*;

class ContentOrganizationServiceTest {

    private Path tempDir;
    private ContentOrganizationService service;
    private ContentOrganizationRepository repository;

    @BeforeEach
    void setUp() throws IOException {
        tempDir = Files.createTempDirectory("surrogate-test-");
        repository = new InMemoryContentOrganizationRepository(); // Assuming an in-memory implementation for testing
        service = new ContentOrganizationService(repository, tempDir);
    }

    @AfterEach
    void tearDown() throws IOException {
        // Clean up any leftover files/directories
        if (Files.exists(tempDir)) {
            Files.walk(tempDir)
                 .sorted(Comparator.reverseOrder())
                 .forEach(p -> {
                     try {
                         Files.deleteIfExists(p);
                     } catch (IOException ignored) {}
                 });
        }
    }

    @Test
    void deleteRecordedStream_RemovesFileSecurely() throws IOException {
        // Arrange: create a dummy recorded stream file
        String streamId = "test-stream.dat";
        Path streamFile = tempDir.resolve(streamId);
        Files.write(streamFile, "dummy content".getBytes());

        assertTrue(Files.exists(streamFile), "Precondition: file should exist before deletion");

        // Act
        service.deleteRecordedStream(streamId);

        // Assert
        assertFalse(Files.exists(streamFile), "File should be removed after deletion");
    }

    @Test
    void deleteRecordedStream_NonExistentThrows() {
        String missingId = "nonexistent.dat";
        assertThrows(java.io.FileNotFoundException.class,
                () -> service.deleteRecordedStream(missingId));
    }

    @Test
    void deleteRecordedStream_PathTraversalIsBlocked() throws IOException {
        // Attempt to delete a file outside the storage root using ".."
        String maliciousId = "../malicious-file.dat";
        assertThrows(SecurityException.class,
                () -> service.deleteRecordedStream(maliciousId));
    }

    @Test
    void getRecordedStreams_ReturnsEmptyListInitially() {
        List<String> streams = service.getRecordedStreams();
        assertNotNull(streams);
        assertTrue(streams.isEmpty());
    }
}