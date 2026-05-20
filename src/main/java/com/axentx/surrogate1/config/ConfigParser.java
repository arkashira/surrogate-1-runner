package com.axentx.surrogate1.config;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;
import java.util.regex.Pattern;

public class ConfigParser {
    private static final String CONFIG_PATH = "/etc/axentx/surrogate-1/freerouter.conf";
    private static final String DEFAULT_JVM_HEAP_SIZE = "2g";
    private static final String DEFAULT_JVM_METASPACE_SIZE = "256m";
    private static final Pattern JVM_SIZE_PATTERN = Pattern.compile("^\\d+(m|g)$");

    public static JVMConfig parseJVMConfig() {
        Properties props = new Properties();
        try {
            Path configPath = Paths.get(CONFIG_PATH);
            if (Files.exists(configPath)) {
                props.load(Files.newInputStream(configPath));
            }
        } catch (IOException e) {
            // Log error or handle appropriately
            System.err.println("Failed to load configuration: " + e.getMessage());
            return null; // Return null or throw an exception based on the application's needs
        }

        String heapSize = getJVMSize(props, "jvm.heap.size", DEFAULT_JVM_HEAP_SIZE);
        String metaspaceSize = getJVMSize(props, "jvm.metaspace.size", DEFAULT_JVM_METASPACE_SIZE);

        if (heapSize == null || metaspaceSize == null) {
            // Log error or handle appropriately
            System.err.println("Invalid JVM size configuration");
            return null; // Return null or throw an exception based on the application's needs
        }

        return new JVMConfig(heapSize, metaspaceSize);
    }

    private static String getJVMSize(Properties props, String key, String defaultValue) {
        String size = props.getProperty(key, defaultValue);
        if (!JVM_SIZE_PATTERN.matcher(size).matches()) {
            return null; // Invalid JVM size format
        }
        return size;
    }

    public static class JVMConfig {
        private final String heapSize;
        private final String metaspaceSize;

        public JVMConfig(String heapSize, String metaspaceSize) {
            this.heapSize = heapSize;
            this.metaspaceSize = metaspaceSize;
        }

        public String getHeapSize() {
            return heapSize;
        }

        public String getMetaspaceSize() {
            return metaspaceSize;
        }
    }
}