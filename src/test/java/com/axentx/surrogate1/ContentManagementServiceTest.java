package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import java.nio.file.Path;
import java.io.IOException;
import static org.junit.jupiter.api.Assertions.*;

public class ContentManagementServiceTest {

    @TempDir
    Path tempDir;

    @Test
    public void testDeleteRecordedStream() throws IOException {
        ContentManagementService service = new ContentManagementService();
        Path testFile = tempDir.resolve("testStream");
        Files.createFile(testFile);

        service.deleteRecordedStream(testFile.toString());
        assertFalse(Files.exists(testFile));
    }

    @Test
    public void testDeleteNonExistentStream() throws IOException {
        ContentManagementService service = new ContentManagementService();
        assertThrows(IOException.class, () -> {
            service.deleteRecordedStream("nonExistentStream");
        });
    }
}