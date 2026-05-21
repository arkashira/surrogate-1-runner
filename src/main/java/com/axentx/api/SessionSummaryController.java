package com.axentx.api;

import com.axentx.service.SessionSummaryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
public class SessionSummaryController {

    @Autowired
    private SessionSummaryService sessionSummaryService;

    @GetMapping("/api/session-summary")
    public List<Map<String, Object>> getSessionSummary(@RequestParam(value = "userId", required = false) String userId) {
        return sessionSummaryService.getSessionSummary(userId);
    }
}