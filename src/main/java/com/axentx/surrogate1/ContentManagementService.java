package com.axentx.surrogate1;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ContentManagementService {

    private static final String STORAGE_PATH = "/path/to/storage";

    public void deleteRecordedStream(String streamId) throws IOException {
        Path streamPath = Paths.get(STORAGE_PATH, streamId);
        if (Files.exists(streamPath)) {
            // Secure deletion by overwriting the file before deleting
            secureDelete(streamPath);
            Files.delete(streamPath);
        } else {
            throw new IOException("Stream not found: " + streamId);
        }
    }

    private void secureDelete(Path path) throws IOException {
        // Overwrite the file with zeros to ensure secure deletion
        byte[] zeros = new byte[1024];
        try (java.io.FileOutputStream fos = new java.io.FileOutputStream(path.toFile())) {
            while (fos.write(zeros) != -1) {
                // Continue overwriting
            }
        }
    }
}