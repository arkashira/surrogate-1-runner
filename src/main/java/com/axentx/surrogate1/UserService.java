package com.axentx.surrogate1;

import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class UserService {

    // Simple in‑memory store: username -> password
    private final Map<String, String> users = new ConcurrentHashMap<>();

    /**
     * Registers a new user.
     *
     * @param username the desired username
     * @param password the desired password
     * @return true if registration succeeded, false if username already exists
     */
    public boolean register(String username, String password) {
        return users.putIfAbsent(username, password) == null;
    }

    /**
     * Validates a login attempt.
     *
     * @param username the username
     * @param password the password
     * @return true if credentials match an existing user
     */
    public boolean login(String username, String password) {
        String stored = users.get(username);
        return stored != null && stored.equals(password);
    }

    /**
     * Resets a user's password.
     *
     * @param username    the username
     * @param newPassword the new password
     * @return true if the user existed and password was updated
     */
    public boolean resetPassword(String username, String newPassword) {
        return users.computeIfPresent(username, (k, v) -> newPassword) != null;
    }
}