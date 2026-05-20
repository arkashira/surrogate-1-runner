package com.axentx.surrogate1.ui.model;

public class Alert {
    private String id;
    private String severity;
    private String timestamp;
    private String description;

    public Alert(String id, String severity, String timestamp, String description) {
        this.id = id;
        this.severity = severity;
        this.timestamp = timestamp;
        this.description = description;
    }

    // ----- getters & setters -----
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }

    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}