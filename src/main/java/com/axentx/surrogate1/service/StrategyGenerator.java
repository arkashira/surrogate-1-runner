package com.axentx.surrogate1.service;

import com.axentx.surrogate1.model.BusinessDetails;
import com.axentx.surrogate1.model.MarketingStrategy;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class StrategyGenerator {

    private static final List<String> MARKETING_CHANNELS = Arrays.asList(
            "Social Media Marketing", "Content Marketing", "Email Marketing",
            "Search Engine Optimization (SEO)", "Pay-Per-Click Advertising (PPC)",
            "Influencer Partnerships", "Referral Programs", "Webinars and Events",
            "Video Marketing", "Podcast Marketing"
    );

    private static final Map<String, List<String>> INDUSTRY_STRATEGIES = new HashMap<>();
    private static final Map<String, List<String>> GOAL_STRATEGIES = new HashMap<>();

    static {
        INDUSTRY_STRATEGIES.put("SaaS", Arrays.asList(
                "Freemium Model", "Customer Success Stories", "API Integration Marketing",
                "User Onboarding Campaigns", "Churn Reduction Strategies"
        ));
        INDUSTRY_STRATEGIES.put("E-commerce", Arrays.asList(
                "Seasonal Promotions", "Abandoned Cart Recovery", "Product Recommendations",
                "Customer Reviews & Testimonials", "Cross-Selling Strategies"
        ));
        INDUSTRY_STRATEGIES.put("Healthcare", Arrays.asList(
                "Patient Education Content", "Telehealth Promotion", "Insurance Partnership",
                "Community Health Events", "Medical Professional Referrals"
        ));
        INDUSTRY_STRATEGIES.put("Finance", Arrays.asList(
                "Financial Literacy Content", "Investment Advisory Services", "Credit Card Promotions",
                "Retirement Planning Campaigns", "Personal Finance Apps"
        ));

        GOAL_STRATEGIES.put("Brand Awareness", Arrays.asList(
                "Social Media Contests", "Influencer Collaborations", "Public Relations",
                "Event Sponsorships", "Content Series Launches"
        ));
        GOAL_STRATEGIES.put("Lead Generation", Arrays.asList(
                "Lead Magnets", "Webinar Series", "SEO Landing Pages", "PPC Campaigns",
                "Email Capture Forms"
        ));
        GOAL_STRATEGIES.put("Revenue Growth", Arrays.asList(
                "Upselling & Cross-selling", "Subscription Models", "Premium Features",
                "Bundle Pricing", "Customer Retention Programs"
        ));
        GOAL_STRATEGIES.put("Customer Retention", Arrays.asList(
                "Loyalty Programs", "Regular Check-ins", "Exclusive Offers", "Feedback Loops",
                "Customer Success Teams"
        ));
    }

    public List<MarketingStrategy> generateStrategies(BusinessDetails businessDetails) {
        List<MarketingStrategy> strategies = new ArrayList<>();

        String industry = businessDetails.getIndustry();
        String goal = businessDetails.getGoal();

        // Generate core strategies based on industry
        if (INDUSTRY_STRATEGIES.containsKey(industry)) {
            List<String> industryStrategies = INDUSTRY_STRATEGIES.get(industry);
            for (int i = 0; i < Math.min(2, industryStrategies.size()); i++) {
                strategies.add(new MarketingStrategy(
                        "Industry-Specific Strategy",
                        industryStrategies.get(i),
                        "Tailored approach for " + industry + " industry"
                ));
            }
        }

        // Generate goal-based strategies
        if (GOAL_STRATEGIES.containsKey(goal)) {
            List<String> goalStrategies = GOAL_STRATEGIES.get(goal);
            for (int i = 0; i < Math.min(2, goalStrategies.size()); i++) {
                strategies.add(new MarketingStrategy(
                        "Goal-Oriented Strategy",
                        goalStrategies.get(i),
                        "Focused approach to achieve " + goal + " objective"
                ));
            }
        }

        // Add channel strategies
        Random random = new Random();
        int numChannels = Math.min(3, MARKETING_CHANNELS.size());
        Set<String> selectedChannels = new HashSet<>();
        
        while (selectedChannels.size() < numChannels) {
            String channel = MARKETING_CHANNELS.get(random.nextInt(MARKETING_CHANNELS.size()));
            selectedChannels.add(channel);
        }

        for (String channel : selectedChannels) {
            strategies.add(new MarketingStrategy(
                    "Channel Strategy",
                    channel,
                    "Implementation approach for " + channel
            ));
        }

        // Add general strategies
        strategies.add(new MarketingStrategy(
                "General Strategy",
                "Data-Driven Marketing Approach",
                "Use analytics to optimize campaigns and measure ROI"
        ));

        strategies.add(new MarketingStrategy(
                "General Strategy",
                "Customer Journey Mapping",
                "Understand customer touchpoints and improve experience"
        ));

        return strategies;
    }
}