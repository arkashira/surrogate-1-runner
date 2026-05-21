package com.axentx.surrogate1.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
public class SessionController {

    @GetMapping("/sessions")
    public List<String> getSessionList() {
        // Placeholder logic to fetch active sessions
        return List.of("session1", "session2", "session3");
    }
}