
package com.axentx.surrogate1.recommendation;

public class Recommendation {
    private final String description;
    private final String action;

    public Recommendation(String description, String action) {
        this.description = description;
        this.action = action;
    }

    public String getDescription() {
        return description;
    }

    public String getAction() {
        return action;
    }
}