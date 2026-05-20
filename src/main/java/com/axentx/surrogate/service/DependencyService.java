package com.axentx.surrogate.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class DependencyService {
    private static final Logger logger = LoggerFactory.getLogger(DependencyService.class);

    public void logDependencyChange(String dependency, String oldVersion, String newVersion) {
        logger.info("Dependency change: {} from {} to {}", dependency, oldVersion, newVersion);
    }
}