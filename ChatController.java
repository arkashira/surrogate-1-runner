package com.example.chat.controller;

import com.example.chat.service.ChatService;
import com.example.chat.service.ChatService.Message;
import org.springframework.messaging.handler.annotation.*;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;

@Controller
public class ChatController {

    private final SimpMessagingTemplate template;
    private final ChatService service;

    public ChatController(SimpMessagingTemplate template, ChatService service) {
        this.template = template;
        this.service = service;
    }

    // Client sends to /app/message
    @MessageMapping("/message")
    public void handleMessage(@Payload Message msg) {
        // Persist
        service.addMessage(msg);
        // Broadcast to all subscribers
        template.convertAndSend("/topic/messages", msg);
    }

    // Optional: expose history via REST (for initial load)
    @MessageMapping("/history")
    @SendTo("/topic/history")
    public List<Message> history() {
        return service.getHistory();
    }
}