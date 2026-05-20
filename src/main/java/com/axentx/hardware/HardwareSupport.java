package com.axentx.hardware;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/**
 * Utility class to determine if the current hardware configuration
 * supports a given GPU architecture. This is a simplified stub
 * used for compatibility testing. In a real system, this would
 * query the actual GPU driver or hardware capabilities.
 */
public class HardwareSupport {

    /**
     * Set of GPU architectures that are considered supported
     * by the current hardware. These are placeholder values
     * representing upcoming GPU families.
     */
    private static final Set<String> SUPPORTED_ARCHITECTURES;

    static {
        Set<String> archs = new HashSet<>();
        archs.add("Ada Lovelace");   // NVIDIA RTX 40 series
        archs.add("RDNA 3");          // AMD Radeon RX 7000 series
        archs.add("Xe-HPG");          // Intel Arc series
        archs.add("Sapphire Rapids"); // Hypothetical future CPU+GPU platform
        SUPPORTED_ARCHITECTURES = Collections.unmodifiableSet(archs);
    }

    /**
     * Checks if the specified GPU architecture is supported.
     *
     * @param architecture the name of the GPU architecture
     * @return true if supported, false otherwise
     */
    public boolean supportsArchitecture(String architecture) {
        if (architecture == null) {
            return false;
        }
        return SUPPORTED_ARCHITECTURES.contains(architecture.trim());
    }
}