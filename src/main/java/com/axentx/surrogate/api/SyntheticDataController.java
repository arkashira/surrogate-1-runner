package com.axentx.surrogate.api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.axentx.surrogate.service.SyntheticDataService;

@RestController
public class SyntheticDataController {

    private final SyntheticDataService syntheticDataService;

    public SyntheticDataController(SyntheticDataService syntheticDataService) {
        this.syntheticDataService = syntheticDataService;
    }

    @GetMapping("/api/synthetic-data")
    public String getSyntheticData(@RequestParam String integrationType) {
        return syntheticDataService.generateSyntheticData(integrationType);
    }
}