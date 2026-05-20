package com.axentx.surrogate1;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class UserRegistration {

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public User register(String email, String password) {
        String encodedPassword = passwordEncoder.encode(password);
        return new User(UUID.randomUUID().toString(), email, encodedPassword);
    }
}