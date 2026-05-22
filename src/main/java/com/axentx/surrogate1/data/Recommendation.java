package com.axentx.surrogate1.data;

public class Recommendation {
    private final String description;
    private final String reason;

    public Recommendation(String description, String reason) {
        this.description = description;
        this.reason = reason;
    }

    public String getDescription() {
        return description;
    }

    public String getReason() {
        return reason;
    }

    @Override
    public String toString() {
        return "Recommendation{" +
                "description='" + description + '\'' +
                ", reason='" + reason + '\'' +
                '}';
    }
}