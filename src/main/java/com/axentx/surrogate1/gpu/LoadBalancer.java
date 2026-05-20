package com.axentx.surrogate1.gpu;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

/**
 * Detects available GPUs on the system and configures a simple round‑robin
 * load‑balancing scheme for downstream components.
 *
 * The detection uses {@code nvidia-smi} which is present on supported
 * firmware images. The resulting mapping is stored as a system property
 * {@code axentx.gpu.loadbalancer.mapping} in the form:
 *
 * {@code 0:GPU-Name0,1:GPU-Name1,...}
 *
 * Downstream code can read this property to distribute work across GPUs.
 */
public class LoadBalancer {

    private static final Logger logger = Logger.getLogger(LoadBalancer.class.getName());

    /**
     * Detects GPUs using {@code nvidia-smi}.
     *
     * @return a list of GPU names; empty if none are found or an error occurs.
     */
    public List<String> detectGPUs() {
        List<String> gpus = new ArrayList<>();
        ProcessBuilder pb = new ProcessBuilder(
                "nvidia-smi",
                "--query-gpu=name",
                "--format=csv,noheader"
        );
        pb.redirectErrorStream(true);
        try {
            Process proc = pb.start();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(proc.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    line = line.trim();
                    if (!line.isEmpty()) {
                        gpus.add(line);
                    }
                }
            }
            int exitCode = proc.waitFor();
            if (exitCode != 0) {
                logger.warning("nvidia-smi exited with non‑zero code: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            logger.severe("Failed to execute nvidia-smi: " + e.getMessage());
        }
        logger.info("Detected GPUs: " + gpus);
        return gpus;
    }

    /**
     * Configures a round‑robin load‑balancing mapping for the supplied GPUs.
     * The mapping is stored as a system property for consumption by other
     * components.
     *
     * @param gpus list of GPU identifiers (names). If empty, no configuration
     *             is performed.
     */
    public void configureLoadBalancing(List<String> gpus) {
        if (gpus == null || gpus.isEmpty()) {
            logger.warning("No GPUs detected – skipping load‑balancing configuration.");
            return;
        }

        StringBuilder mapping = new StringBuilder();
        for (int i = 0; i < gpus.size(); i++) {
            mapping.append(i).append(":").append(gpus.get(i));
            if (i < gpus.size() - 1) {
                mapping.append(",");
            }
        }

        System.setProperty("axentx.gpu.loadbalancer.mapping", mapping.toString());
        logger.info("Configured GPU load‑balancing mapping: " + mapping);
    }

    /**
     * Convenience method to be called at system boot. Detects GPUs and
     * configures the load‑balancing mapping automatically.
     */
    public void initialize() {
        List<String> gpus = detectGPUs();
        configureLoadBalancing(gpus);
    }
}