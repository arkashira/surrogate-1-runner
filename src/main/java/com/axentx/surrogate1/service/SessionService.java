package com.axentx.surrogate1.service;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

public class SessionService {

    private final ConcurrentMap<String, Session> sessions;

    public SessionService() {
        this.sessions = new ConcurrentHashMap<>();
    }

    public void terminateSession(String sessionId) {
        Session session = sessions.get(sessionId);
        if (session != null) {
            session.close();
            sessions.remove(sessionId);
        }
    }

    public void addSession(String sessionId, Session session) {
        sessions.put(sessionId, session);
    }
}