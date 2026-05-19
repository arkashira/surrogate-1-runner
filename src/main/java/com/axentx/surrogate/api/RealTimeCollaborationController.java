package com.axentx.surrogate.api;

import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
@RequestMapping("/api/collaboration")
public class RealTimeCollaborationController {

    private final SimpMessagingTemplate messagingTemplate;

    public RealTimeCollaborationController(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;
    }

    @MessageMapping("/debug")
    @SendTo("/topic/debug")
    public DebugMessage handleDebugMessage(@RequestBody DebugMessage message) {
        if (message.getContent() == null || message.getSender() == null) {
            throw new IllegalArgumentException("Both content and sender must be provided.");
        }
        return message;
    }

    @MessageMapping("/refine")
    @SendTo("/topic/refine")
    public RefineMessage handleRefineMessage(@RequestBody RefineMessage message) {
        if (message.getContent() == null || message.getSender() == null) {
            throw new IllegalArgumentException("Both content and sender must be provided.");
        }
        return message;
    }

    @RequestMapping(method = RequestMethod.POST, value = "/join")
    public void joinCollaboration(@RequestBody JoinRequest request) {
        if (request.getUserId() == null || request.getSessionId() == null) {
            throw new IllegalArgumentException("Both userId and sessionId must be provided.");
        }
        messagingTemplate.convertAndSend("/topic/collaboration", request);
    }
}

class DebugMessage {
    private String content;
    private String sender;

    // Getters and Setters
}

class RefineMessage {
    private String content;
    private String sender;

    // Getters and Setters
}

class JoinRequest {
    private String userId;
    private String sessionId;

    // Getters and Setters
}