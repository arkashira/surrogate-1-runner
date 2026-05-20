package com.axentx.surrogate1.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.ArrayList;
import java.util.List;

/**
 * Exposes the /cost-optimizations page.
 * In a real system this would call a recommendation engine.
 */
@Controller
public class RecommendationController {

    /**
     * DTO representing a single recommendation.
     */
    public static class Recommendation {
        private final String instanceId;
        private final String currentType;
        private final String suggestedType;
        private final String region;
        private final double monthlySavings;
        private final String costinelLink;

        public Recommendation(String instanceId,
                               String currentType,
                               String suggestedType,
                               String region,
                               double monthlySavings,
                               String costinelLink) {
            this.instanceId = instanceId;
            this.currentType = currentType;
            this.suggestedType = suggestedType;
            this.region = region;
            this.monthlySavings = monthlySavings;
            this.costinelLink = costinelLink;
        }

        public String getInstanceId() { return instanceId; }
        public String getCurrentType() { return currentType; }
        public String getSuggestedType() { return suggestedType; }
        public String getRegion() { return region; }
        public double getMonthlySavings() { return monthlySavings; }
        public String getCostinelLink() { return costinelLink; }
    }

    /**
     * GET /cost-optimizations
     */
    @GetMapping("/cost-optimizations")
    public String getCostOptimizations(Model model) {
        // TODO: Replace this mock list with a real recommendation engine call
        List<Recommendation> recommendations = new ArrayList<>();
        recommendations.add(new Recommendation(
                "i-0abcd1234efgh5678",
                "m5.large",
                "m5.xlarge",
                "us-east-1",
                1200.00,
                "https://costinel.example.com/apply?instanceId=i-0abcd1234efgh5678&target=m5.xlarge"
        ));

        model.addAttribute("recommendations", recommendations);
        return "costOptimizations";
    }
}