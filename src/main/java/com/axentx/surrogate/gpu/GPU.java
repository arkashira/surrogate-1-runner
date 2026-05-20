package com.axentx.surrogate.gpu;

public class GPU {
    private String id;
    private String manufacturer;
    private String model;
    private int memory;

    public GPU(String id, String manufacturer, String model, int memory) {
        this.id = id;
        this.manufacturer = manufacturer;
        this.model = model;
        this.memory = memory;
    }

    // Getters and setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public int getMemory() {
        return memory;
    }

    public void setMemory(int memory) {
        this.memory = memory;
    }
}