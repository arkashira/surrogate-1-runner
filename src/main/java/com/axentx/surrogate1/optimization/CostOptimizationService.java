package com.axentx.surrogate1.optimization;

import com.axentx.surrogate1.model.Session;
import com.axentx.surrogate1.model.CostOptimizationActivity;
import com.axentx.surrogate1.repository.SessionRepository;
import com.axentx.surrogate1.repository.CostOptimizationActivityRepository;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Periodically scans active sessions, applies {@link CostOptimizer},
 * and persists any optimisation activities.
 *
 * Runs without human intervention.
 */
@Component
public class CostOptimizationService {

    private final SessionRepository sessionRepository;
    private final CostOptimizationActivityRepository activityRepository;

    public CostOptimizationService(SessionRepository sessionRepository,
                                   CostOptimizationActivityRepository activityRepository) {
        this.sessionRepository = sessionRepository;
        this.activityRepository = activityRepository;
    }

    /**
     * Executes every minute. Adjust the rate as needed.
     */
    @Scheduled(fixedRateString = "${cost.optimization.interval.ms:60000}")
    public void runOptimizationCycle() {
        List<Session> activeSessions = sessionRepository.findAllActive();
        for (Session session : activeSessions) {
            CostOptimizationActivity activity = CostOptimizer.optimize(session);
            if (activity != null) {
                // Persist changes to the session and the activity log
                sessionRepository.save(session);
                activityRepository.save(activity);
            }
        }
    }
}