package com.example.cloudopt;

public final class Recommendation {
    private final String title;
    private final String description;
    private final Runnable action;   // side‑effectful, but isolated

    public Recommendation(String title, String description, Runnable action) {
        this.title = title;
        this.description = description;
        this.action = action;
    }

    public String getTitle()      { return title; }
    public String getDescription(){ return description; }

    /** Execute the recommendation.  In production this would call the cloud API. */
    public void apply() { action.run(); }
}