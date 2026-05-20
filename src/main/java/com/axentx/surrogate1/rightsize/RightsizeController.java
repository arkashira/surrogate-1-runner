package com.axentx.surrogate1.rightsize;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
public class RightsizeController {

    private final RightsizeService rightsizeService;

    public RightsizeController(RightsizeService rightsizeService) {
        this.rightsizeService = rightsizeService;
    }

    @GetMapping("/api/rightsize")
    public List<Recommendation> getRecommendations() {
        return rightsizeService.getRecommendations();
    }
}