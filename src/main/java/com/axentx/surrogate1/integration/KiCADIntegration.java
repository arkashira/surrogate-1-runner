package com.axentx.surrogate1.integration;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

public class KiCADIntegration {
    private static final Logger LOGGER = Logger.getLogger(KiCADIntegration.class.getName());
    private static final String KICAD_VERSION_COMMAND = "kicad --version";
    private static final String KICAD_VERSION_REQUIRED = "9";

    /**
     * Checks if the installed KiCAD version meets the minimum requirement.
     * @return true if compatible, false otherwise.
     */
    public boolean isKiCADVersionCompatible() {
        try {
            Process process = Runtime.getRuntime().exec(KICAD_VERSION_COMMAND);
            
            // Use try-with-resources to ensure the reader is closed automatically
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    // Basic check for version string. 
                    // Note: For production, consider using regex to ensure exact version matching (e.g., "^KiCad 9\\.")
                    if (line.contains(KICAD_VERSION_REQUIRED)) {
                        return true;
                    }
                }
            }
            
            // Wait for the version check process to finish
            process.waitFor();
        } catch (IOException | InterruptedException e) {
            LOGGER.log(Level.SEVERE, "Error checking KiCAD version", e);
        }
        return false;
    }

    /**
     * Launches Freerouter if the KiCAD version is compatible.
     * This method starts the process in the background to avoid blocking the application.
     */
    public void launchFreerouter() {
        if (!isKiCADVersionCompatible()) {
            LOGGER.warning("KiCAD version incompatible. Cannot launch Freerouter.");
            return;
        }

        try {
            // Use ProcessBuilder for better control over the execution environment
            ProcessBuilder pb = new ProcessBuilder("freerouter");
            
            // Start the process but do NOT wait for it to finish.
            // This allows the Java application to continue running while Freerouter opens.
            Process process = pb.start();
            
            LOGGER.info("Freerouter launched successfully. Process ID: " + process.pid());

        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Failed to launch Freerouter", e);
        }
    }
}