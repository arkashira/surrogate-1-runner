
package com.axentx.surrogate1;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class HardwareDatabase {
    private static final Map<String, HardwareSpec> hardwareSpecs = new ConcurrentHashMap<>();

    static {
        // Add your hardware specifications here.
        // Each entry should be of the form:
        // hardwareSpecs.put("hardware-id", new HardwareSpec("hardware-name", "manufacturer", "model", "price"));
    }

    public static HardwareSpec getHardwareSpec(String hardwareId) {
        return hardwareSpecs.get(hardwareId);
    }

    public static void addHardwareSpec(HardwareSpec hardwareSpec) {
        hardwareSpecs.put(hardwareSpec.getId(), hardwareSpec);
    }

    public static class HardwareSpec {
        private final String id;
        private final String name;
        private final String manufacturer;
        private final String model;
        private final double price;

        public HardwareSpec(String id, String name, String manufacturer, String model, double price) {
            this.id = id;
            this.name = name;
            this.manufacturer = manufacturer;
            this.model = model;
            this.price = price;
        }

        public String getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public String getManufacturer() {
            return manufacturer;
        }

        public String getModel() {
            return model;
        }

        public double getPrice() {
            return price;
        }
    }
}