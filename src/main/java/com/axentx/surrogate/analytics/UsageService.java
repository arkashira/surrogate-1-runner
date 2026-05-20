package com.axentx.surrogate.analytics;

import com.axentx.surrogate.domain.Pipeline;
import com.axentx.surrogate.domain.PipelineRun;
import com.axentx.surrogate.repository.PipelineRepository;
import com.axentx.surrogate.repository.PipelineRunRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.server.standard.ServerEndpoint;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Service
public class UsageService {

    private final PipelineRepository pipelineRepository;
    private final PipelineRunRepository pipelineRunRepository;

    private final Map<String, WebSocketSession> activeSessions = new ConcurrentHashMap<>();
    private final Map<String, UsageStatistics> cachedStatistics = new ConcurrentHashMap<>();

    @Autowired
    public UsageService(PipelineRepository pipelineRepository, PipelineRunRepository pipelineRunRepository) {
        this.pipelineRepository = pipelineRepository;
        this.pipelineRunRepository = pipelineRunRepository;
    }

    public UsageStatistics getUsageStatistics() {
        Instant thirtyDaysAgo = Instant.now().minus(30, java.time.temporal.ChronoUnit.DAYS);

        List<Pipeline> pipelines = pipelineRepository.findAllByCreatedAtAfter(thirtyDaysAgo);
        List<PipelineRun> runs = pipelineRunRepository.findAllByCreatedAtAfter(thirtyDaysAgo);

        long pipelineCount = pipelines.size();
        long totalDataIngested = runs.stream()
                .mapToLong(PipelineRun::getDataIngestedBytes)
                .sum();

        double averageRunTime = runs.stream()
                .mapToLong(PipelineRun::getDurationMs)
                .average()
                .orElse(0.0);

        return new UsageStatistics(pipelineCount, totalDataIngested, averageRunTime);
    }

    public void broadcastStatistics() {
        for (WebSocketSession session : activeSessions.values()) {
            try {
                UsageStatistics stats = getUsageStatistics();
                session.sendMessage(new TextMessage("{\"type\":\"usage_update\",\"data\":" + 
                    "{\"pipelines\":" + stats.pipelineCount + 
                    ",\"totalDataIngested\":" + stats.totalDataIngested + 
                    ",\"averageRunTime\":" + stats.averageRunTime + "}}}"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public void registerSession(String userId, WebSocketSession session) {
        activeSessions.put(userId, session);
    }

    public void unregisterSession(String userId) {
        activeSessions.remove(userId);
    }

    public void sendLiveUpdate(String userId) {
        WebSocketSession session = activeSessions.get(userId);
        if (session != null) {
            try {
                UsageStatistics stats = getUsageStatistics();
                session.sendMessage(new TextMessage("{\"type\":\"usage_update\",\"data\":" + 
                    "{\"pipelines\":" + stats.pipelineCount + 
                    ",\"totalDataIngested\":" + stats.totalDataIngested + 
                    ",\"averageRunTime\":" + stats.averageRunTime + "}}}"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @ServerEndpoint("/ws/usage")
    public static class UsageWebSocketHandler extends TextWebSocketHandler {
        
        private final UsageService usageService;

        public UsageWebSocketHandler(UsageService usageService) {
            this.usageService = usageService;
        }

        @Override
        public void afterConnectionEstablished(WebSocketSession session) {
            String userId = session.getAttributes().get("userId").toString();
            usageService.registerSession(userId, session);
            usageService.broadcastStatistics();
        }

        @Override
        public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
            String userId = session.getAttributes().get("userId").toString();
            usageService.unregisterSession(userId);
        }

        @Override
        public void handleTextMessage(WebSocketSession session, TextMessage message) {
            String payload = message.getPayload();
            if (payload.equals("refresh")) {
                String userId = session.getAttributes().get("userId").toString();
                usageService.sendLiveUpdate(userId);
            }
        }
    }

    public static class UsageStatistics {
        public final long pipelineCount;
        public final long totalDataIngested;
        public final double averageRunTime;

        public UsageStatistics(long pipelineCount, long totalDataIngested, double averageRunTime) {
            this.pipelineCount = pipelineCount;
            this.totalDataIngested = totalDataIngested;
            this.averageRunTime = averageRunTime;
        }
    }
}