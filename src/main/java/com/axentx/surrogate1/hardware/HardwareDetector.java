package com.axentx.surrogate1.hardware;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class HardwareDetector {

    public static String detectHardwareConfiguration() {
        StringBuilder hardwareInfo = new StringBuilder();

        try {
            // Detect CPU information
            hardwareInfo.append("CPU Information:\n");
            hardwareInfo.append(executeCommand("cat /proc/cpuinfo"));

            // Detect memory information
            hardwareInfo.append("\nMemory Information:\n");
            hardwareInfo.append(executeCommand("cat /proc/meminfo"));

            // Detect GPU information if available
            hardwareInfo.append("\nGPU Information:\n");
            hardwareInfo.append(executeCommand("lspci | grep -i vga"));

            // Detect disk information
            hardwareInfo.append("\nDisk Information:\n");
            hardwareInfo.append(executeCommand("lsblk"));

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return hardwareInfo.toString();
    }

    private static String executeCommand(String command) throws IOException, InterruptedException {
        Process process = Runtime.getRuntime().exec(command);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }

        process.waitFor();
        return output.toString();
    }
}