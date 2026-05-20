package com.axentx.surrogate1;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.Random;

public class ContentOrganizationService {

    private final ContentOrganizationRepository repository;
    private final Path storageRoot;

    public ContentOrganizationService(ContentOrganizationRepository repository, Path storageRoot) {
        this.repository = repository;
        this.storageRoot = storageRoot;
    }

    /**
     * Securely deletes a recorded stream identified by {@code streamId}.
     *
     * <p>The method performs the following steps:
     * <ol>
     *   <li>Resolve the absolute path of the stream under {@code storageRoot}.</li>
     *   <li>Verify that the file exists; otherwise throws {@link java.io.FileNotFoundException}.</li>
     *   <li>Overwrite the entire file with random bytes (secure delete).</li>
     *   <li>Delete the file from the filesystem.</li>
     * </ol>
     *
     * @param streamId the identifier of the recorded stream to delete
     * @throws IOException if an I/O error occurs during the operation
     */
    public void deleteRecordedStream(String streamId) throws IOException {
        Path streamPath = storageRoot.resolve(streamId).normalize();

        // Ensure the resolved path is still within the storage root to prevent path traversal attacks
        if (!streamPath.startsWith(storageRoot)) {
            throw new SecurityException("Attempted to delete a path outside of storage root");
        }

        if (!Files.isRegularFile(streamPath)) {
            throw new java.io.FileNotFoundException("Recorded stream not found: " + streamId);
        }

        // Secure overwrite with random data
        long size = Files.size(streamPath);
        Random random = new Random();

        try (OutputStream out = Files.newOutputStream(streamPath,
                StandardOpenOption.WRITE, StandardOpenOption.TRUNCATE_EXISTING)) {
            byte[] buffer = new byte[8192];
            long written = 0;
            while (written < size) {
                random.nextBytes(buffer);
                int toWrite = (int) Math.min(buffer.length, size - written);
                out.write(buffer, 0, toWrite);
                written += toWrite;
            }
            out.flush();
        }

        // Delete the file permanently
        Files.delete(streamPath);

        // Notify the repository about the deletion
        repository.deleteRecordedStream(streamId);
    }

    public List<String> getRecordedStreams() {
        return repository.getRecordedStreams();
    }
}