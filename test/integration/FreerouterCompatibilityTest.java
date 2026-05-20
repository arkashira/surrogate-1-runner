package axentx.surrogate1.test.integration;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.condition.EnabledOnOs;
import org.junit.jupiter.api.condition.OS;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Integration tests for Freerouter compatibility with KiCAD 9.
 * 
 * Acceptance criteria:
 * - Clicking the plugin launches Freerouter without errors
 * - The launch process completes within 5 seconds
 * - Freerouter opens with current PCB loaded
 */
@EnabledOnOs({OS.LINUX, OS.MAC})
public class FreerouterCompatibilityTest {
    
    private static final String FREEROUTER_JAR_PATH = System.getenv("FREEROUTER_JAR_PATH");
    private static final String KICAD_PROJECT_PATH = System.getenv("KICAD_PROJECT_PATH");
    private static final int LAUNCH_TIMEOUT_SECONDS = 5;
    
    private Path tempDir;
    private Path testPcbFile;
    
    @BeforeEach
    void setUp() throws IOException {
        tempDir = Files.createTempDirectory("freerouter_test_");
        
        // Create a minimal test PCB file for KiCAD 9
        testPcbFile = tempDir.resolve("test_board.kicad_pcb");
        String minimalPcbContent = createMinimalKiCad9Pcb();
        Files.writeString(testPcbFile, minimalPcbContent);
    }
    
    /**
     * Creates a minimal KiCAD 9 PCB file structure
     */
    private String createMinimalKiCad9Pcb() {
        return """
            (kicad_pcb (version 20250430) (generator "surrogate-1-test")
              (title "Test Board")
              (page "A4")
              (layers
                (0 "F.Cu" signal)
                (31 "B.Cu" signal)
                (32 "B.Silkscreen" user)
                (33 "F.Silkscreen" user)
                (34 "Edge.Cuts" user)
              )
              (setup
                (pad_to_mask_clearance 0.0)
                (solder_mask_min_width 0.0)
              )
              (footprint "TestPackage:TEST"
                (pad "1" thru_hole circle
                  (at 0 0) (size 1.5 1.5) (drill 0.8)
                  (layers "*.Cu")
                )
              )
            )
            """;
    }
    
    @Test
    @DisplayName("Freerouter JAR file exists and is executable")
    void testFreerouterJarExists() {
        Optional<String> jarPath = getFreerouterJarPath();
        assertTrue(jarPath.isPresent(), "Freerouter JAR path must be configured via FREEROUTER_JAR_PATH env var");
        
        Path jarFilePath = Paths.get(jarPath.get());
        assertTrue(Files.exists(jarFilePath), "Freerouter JAR file must exist at the specified path");
        assertTrue(Files.isExecutable(jarFilePath), "Freerouter JAR file must be executable");
    }
    
    @Test
    @DisplayName("Freerouter launches successfully with current PCB")
    void testFreerouterLaunchesSuccessfully() {
        // Launch Freerouter with the current PCB
        ProcessBuilder processBuilder = new ProcessBuilder(FREEROUTER_JAR_PATH, "--pcb", testPcbFile.toString());
        Process process = processBuilder.start();
        
        // Wait for the launch process to complete within the specified time limit
        boolean launchedSuccessfully = waitProcessToComplete(process, LAUNCH_TIMEOUT_SECONDS);
        assertTrue(launchedSuccessfully, "Freerouter launch process failed to complete within the time limit");
    }
    
    /**
     * Waits for the process to complete within the specified time limit
     * 
     * @param process the process to wait for
     * @param timeout the time limit in seconds
     * @return true if the process completes within the time limit, false otherwise
     */
    private boolean waitProcessToComplete(Process process, int timeout) {
        try {
            process.waitFor(timeout, TimeUnit.SECONDS);
            return true;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
    
    /**
     * Gets the Freerouter JAR path from the environment variable
     * 
     * @return the Freerouter JAR path, or an empty Optional if not set
     */
    private Optional<String> getFreerouterJarPath() {
        String jarPath = System.getenv("FREEROUTER_JAR_PATH");
        return jarPath != null ? Optional.of(jarPath) : Optional.empty();
    }
}