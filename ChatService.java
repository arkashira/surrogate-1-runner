package com.example.chat.service;

import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

@Service
public class ChatService {

    private final List<Message> history = new ArrayList<>();

    public List<Message> getHistory() {
        return new ArrayList<>(history);
    }

    public void addMessage(Message msg) {
        history.add(msg);
    }

    public static record Message(String sender, String text) {}
}