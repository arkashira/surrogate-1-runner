package com.axentx.surrogate1.controller;

import com.axentx.surrogate1.service.SessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ShellController {

    private final SessionService sessionService;

    @Autowired
    public ShellController(SessionService sessionService) {
        this.sessionService = sessionService;
    }

    @PostMapping("/terminate-session")
    public void terminateSession(@RequestBody String sessionId) {
        sessionService.terminateSession(sessionId);
    }
}