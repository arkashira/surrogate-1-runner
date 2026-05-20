package com.axentx.surrogate.service;

import org.springframework.stereotype.Service;
import com.axentx.surrogate.model.SyntheticDataGenerator;

@Service
public class SyntheticDataService {

    private final SyntheticDataGenerator syntheticDataGenerator;

    public SyntheticDataService(SyntheticDataGenerator syntheticDataGenerator) {
        this.syntheticDataGenerator = syntheticDataGenerator;
    }

    public String generateSyntheticData(String integrationType) {
        return syntheticDataGenerator.generate(integrationType);
    }
}