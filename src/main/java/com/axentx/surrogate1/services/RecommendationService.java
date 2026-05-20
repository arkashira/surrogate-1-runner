package com.axentx.surrogate1.services;

import com.axentx.surrogate1.models.MarketingData;
import com.axentx.surrogate1.models.Recommendation;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class RecommendationService {

    public List<Recommendation> generateRecommendations(MarketingData data) {
        List<Recommendation> recommendations = new ArrayList<>();

        // Analyze click-through rate
        if (data.getClickThroughRate() < 0.02) {
            recommendations.add(new Recommendation(
                "Low CTR detected",
                "Your campaign has a low click-through rate. Consider optimizing your ad copy or targeting.",
                "improve_copy_targeting"
            ));
        }

        // Analyze conversion rate
        if (data.getConversionRate() < 0.01) {
            recommendations.add(new Recommendation(
                "Low conversion rate",
                "Your conversion rate is below industry standards. Review your landing page experience.",
                "optimize_landing_page"
            ));
        }

        // Analyze budget efficiency
        if (data.getCostPerAcquisition() > 50.0) {
            recommendations.add(new Recommendation(
                "High CPA detected",
                "Your cost per acquisition is high. Consider adjusting your bidding strategy or targeting.",
                "adjust_bidding_strategy"
            ));
        }

        // Analyze engagement metrics
        if (data.getEngagementScore() < 0.3) {
            recommendations.add(new Recommendation(
                "Low engagement score",
                "Your content isn't resonating with your audience. Try different content formats or topics.",
                "experiment_content_format"
            ));
        }

        // Analyze reach and frequency
        if (data.getReach() < 1000 && data.getFrequency() > 5.0) {
            recommendations.add(new Recommendation(
                "Overexposure risk",
                "Your audience may be getting tired of your ads. Consider refreshing your creative assets.",
                "refresh_creative_assets"
            ));
        }

        // Add general optimization recommendation
        if (recommendations.isEmpty()) {
            recommendations.add(new Recommendation(
                "Performance optimization",
                "Your campaign is performing well. Consider scaling successful elements or testing new variations.",
                "scale_success"
            ));
        }

        return recommendations;
    }
}