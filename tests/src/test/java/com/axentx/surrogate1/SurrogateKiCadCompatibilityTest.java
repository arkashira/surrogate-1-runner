package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Assertions;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Properties;

/**
 * Integration test that validates Surrogate‑1 can run against KiCad 9.
 * The test reads the KiCad executable path from {@code config.yaml},
 * invokes {@code kicad --version}, and asserts the output starts with
 * {@code KiCad 9}.
 *
 * This test is executed in CI as part of the automated workflow.
 */
public class SurrogateKiCadCompatibilityTest {

    private static String kicadExecutable;

    @BeforeAll
    public static void loadConfig() throws Exception {
        // Simple YAML parsing – we only need the "kicad_path" key.
        // The file is expected at the project root under tests/config.yaml.
        String yamlPath = System.getProperty("user.dir") + "/tests/config.yaml";
        if (!Files.exists(Paths.get(yamlPath))) {
            throw new IllegalStateException("Missing config.yaml at " + yamlPath);
        }
        // Very lightweight parsing: each line "key: value"
        for (String line : Files.readAllLines(Paths.get(yamlPath))) {
            line = line.trim();
            if (line.startsWith("kicad_path:")) {
                kicadExecutable = line.split(":", 2)[1].trim();
                break;
            }
        }
        if (kicadExecutable == null || kicadExecutable.isEmpty()) {
            throw new IllegalStateException("kicad_path not defined in config.yaml");
        }
        if (!Files.isExecutable(Paths.get(kicadExecutable))) {
            throw new IllegalStateException("KiCad executable not found or not executable: " + kicadExecutable);
        }
    }

    @Test
    public void testKiCadVersionIs9() throws Exception {
        ProcessBuilder pb = new ProcessBuilder(kicadExecutable, "--version");
        pb.redirectErrorStream(true);
        Process process = pb.start();

        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append('\n');
            }
        }

        int exitCode = process.waitFor();
        Assertions.assertEquals(0, exitCode, "KiCad process exited with non‑zero status");

        String versionOutput = output.toString().trim();
        Assertions.assertTrue(
                versionOutput.startsWith("KiCad 9"),
                "Expected KiCad version 9, but got: " + versionOutput
        );
    }
}