package com.axentx.surrogate1.service;

import com.axentx.surrogate1.domain.UserActivity;
import com.axentx.surrogate1.repository.UserActivityRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class AnalyticsService {

    private final UserActivityRepository userActivityRepository;

    public AnalyticsService(UserActivityRepository userActivityRepository) {
        this.userActivityRepository = userActivityRepository;
    }

    public void logUserSignUp(UUID userId) {
        UserActivity activity = new UserActivity();
        activity.setUserId(userId);
        activity.setActivityType("SIGN_UP");
        activity.setActivityTime(LocalDateTime.now());
        userActivityRepository.save(activity);
    }

    public void logUserLogin(UUID userId) {
        UserActivity activity = new UserActivity();
        activity.setUserId(userId);
        activity.setActivityType("LOGIN");
        activity.setActivityTime(LocalDateTime.now());
        userActivityRepository.save(activity);
    }

    public void logStrategyDownload(UUID userId, UUID strategyId) {
        UserActivity activity = new UserActivity();
        activity.setUserId(userId);
        activity.setActivityType("STRATEGY_DOWNLOAD");
        activity.setActivityTime(LocalDateTime.now());
        activity.setStrategyId(strategyId);
        userActivityRepository.save(activity);
    }

    public void logStrategyView(UUID userId, UUID strategyId) {
        UserActivity activity = new UserActivity();
        activity.setUserId(userId);
        activity.setActivityType("STRATEGY_VIEW");
        activity.setActivityTime(LocalDateTime.now());
        activity.setStrategyId(strategyId);
        userActivityRepository.save(activity);
    }
}