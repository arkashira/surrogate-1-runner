package com.axentx.surrogate.service;

import com.axentx.surrogate.repository.DynamicRoutingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class DynamicRoutingService {

    private final DynamicRoutingRepository dynamicRoutingRepository;

    @Autowired
    public DynamicRoutingService(DynamicRoutingRepository dynamicRoutingRepository) {
        this.dynamicRoutingRepository = dynamicRoutingRepository;
    }

    public Optional<String> routeRequest(String request) {
        List<String> availableAgents = dynamicRoutingRepository.getAvailableAgents();
        if (availableAgents.isEmpty()) {
            return Optional.empty();
        }
        // Simple round-robin for demonstration; replace with cost/scalability optimization logic
        int index = Math.abs(request.hashCode() % availableAgents.size());
        return Optional.of(availableAgents.get(index));
    }

    public void handleAgentAvailabilityChange(String agentId, boolean isAvailable) {
        if (isAvailable) {
            dynamicRoutingRepository.addAgent(agentId);
        } else {
            dynamicRoutingRepository.removeAgent(agentId);
        }
    }
}