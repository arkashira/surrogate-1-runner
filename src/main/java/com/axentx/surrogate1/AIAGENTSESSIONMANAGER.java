package com.axentx.surrogate1;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AIAGENTSESSIONMANAGER {

    @Value("${aiagent.session.cost.threshold}")
    private double costThreshold;

    private final SessionRepository sessionRepository;
    private final AlertService alertService;

    public AIAGENTSESSIONMANAGER(SessionRepository sessionRepository, AlertService alertService) {
        this.sessionRepository = sessionRepository;
        this.alertService = alertService;
    }

    @Scheduled(fixedRate = 300000) // Check every 5 minutes
    public void detectHighCostSessions() {
        List<Session> highCostSessions = sessionRepository.findSessionsAboveCost(costThreshold);
        if (!highCostSessions.isEmpty()) {
            alertService.sendAlert(highCostSessions);
        }
    }
}