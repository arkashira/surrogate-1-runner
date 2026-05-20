package com.axentx.surrogate1.dashboard;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    @Autowired
    private RecommendationService recommendationService;

    @GetMapping("/recommendations")
    public ResponseEntity<List<Map<String, Object>>> getRecommendations() {
        List<Map<String, Object>> recommendations = recommendationService.getRecommendations();
        return ResponseEntity.ok(recommendations);
    }
}