package com.axentx.surrogate1.hardware;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class HardwareProfiler {

    public static String profileHardwarePerformance() {
        StringBuilder performanceInfo = new StringBuilder();

        try {
            // Profile CPU performance
            performanceInfo.append("CPU Performance:\n");
            performanceInfo.append(executeCommand("sysbench --test=cpu --cpu-max-prime=20000 run"));

            // Profile memory performance
            performanceInfo.append("\nMemory Performance:\n");
            performanceInfo.append(executeCommand("sysbench --test=memory --memory-block-size=1K --memory-total-size=10G run"));

            // Profile disk performance
            performanceInfo.append("\nDisk Performance:\n");
            performanceInfo.append(executeCommand("sysbench --test=fileio --file-total-size=1G prepare"));
            performanceInfo.append(executeCommand("sysbench --test=fileio --file-total-size=1G --file-test-mode=rndrw run"));
            performanceInfo.append(executeCommand("sysbench --test=fileio --file-total-size=1G cleanup"));

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return performanceInfo.toString();
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