package com.axentx.surrogate.model;

import java.util.HashMap;
import java.util.Map;

public class SurrogateOptions {
    private Map<String, Object> options;

    public SurrogateOptions(Map<String, Object> options) {
        this.options = options;
    }

    public Map<String, Object> getOptions() {
        return options;
    }
}