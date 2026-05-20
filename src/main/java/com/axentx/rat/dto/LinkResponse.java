package com.axentx.rat.dto;

public class LinkResponse {
    private String error;
    private String linkToken;

    public LinkResponse(String error, String linkToken) {
        this.error = error;
        this.linkToken = linkToken;
    }

    // Getters and Setters
    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getLinkToken() {
        return linkToken;
    }

    public void setLinkToken(String linkToken) {
        this.linkToken = linkToken;
    }
}