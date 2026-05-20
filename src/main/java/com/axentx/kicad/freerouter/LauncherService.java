package com.axentx.kicad.freerouter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

/**
 * Service responsible for launching Freerouter with a given KiCad PCB file.
 *
 * <p>This service provides robust process management including:
 * <ul>
 *   <li>Configurable executable path via Spring configuration</li>
 *   <li>Timeout handling to prevent hanging processes</li>
 *   <li>Input validation</li>
 *   <li>Proper resource cleanup</li>
 * </ul>
 * </p>
 *
 * @author Surrogate-1 Team
 * @version 1.0.0
 */
@Service
public class LauncherService {

    private static final Logger logger = LoggerFactory.getLogger(LauncherService.class);
    private static final long DEFAULT_TIMEOUT_SECONDS = 5;

    @Value("${freerouter.path:/usr/local/bin/freerouter}")
    private String freerouterExecutable;

    @Value("${freerouter.timeout-seconds:5}")
    private long timeoutSeconds;

    /**
     * Launches Freerouter with the specified KiCad PCB file.
     *
     * @param pcbFile the KiCad PCB file to load
     * @return {@code true} if Freerouter launched and exited within the timeout,
     *         {@code false} otherwise
     * @throws IllegalArgumentException if the PCB file is null or doesn't exist
     */
    public boolean launchFreerouter(File pcbFile) {
        validatePcbFile(pcbFile);
        
        Path executablePath = Paths.get(freerouterExecutable);
        if (!executablePath.toFile().exists()) {
            throw new IllegalStateException(
                "Freerouter executable not found at: " + freerouterExecutable
            );
        }

        ProcessBuilder processBuilder = new ProcessBuilder(
            freerouterExecutable,
            "--load", pcbFile.getAbsolutePath()
        );
        processBuilder.redirectErrorStream(true);

        logger.info("Launching Freerouter with PCB file: {}", pcbFile.getAbsolutePath());

        try {
            Process process = processBuilder.start();
            boolean finished = process.waitFor(timeoutSeconds, TimeUnit.SECONDS);
            
            if (!finished) {
                logger.warn("Freerouter process timed out after {} seconds. Forcing termination.", timeoutSeconds);
                process.destroyForcibly();
                return false;
            }

            int exitCode = process.exitValue();
            boolean success = exitCode == 0;
            
            logger.info("Freerouter process completed with exit code: {}", exitCode);
            return success;
            
        } catch (IOException e) {
            logger.error("Failed to start Freerouter process", e);
            Thread.currentThread().interrupt();
            return false;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            logger.error("Launch thread was interrupted", e);
            return false;
        }
    }

    /**
     * Launches Freerouter with the specified PCB file path string.
     *
     * @param pcbPath the path to the KiCad PCB file
     * @return {@code true} if successful, {@code false} otherwise
     */
    public boolean launchFreerouter(String pcbPath) {
        return launchFreerouter(new File(pcbPath));
    }

    private void validatePcbFile(File pcbFile) {
        if (pcbFile == null) {
            throw new IllegalArgumentException("PCB file cannot be null");
        }
        if (!pcbFile.exists()) {
            throw new IllegalArgumentException("PCB file does not exist: " + pcbFile.getAbsolutePath());
        }
        if (!pcbFile.isFile()) {
            throw new IllegalArgumentException("Path is not a file: " + pcbFile.getAbsolutePath());
        }
    }
}