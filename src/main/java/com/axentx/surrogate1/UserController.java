package com.axentx.surrogate1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Minimal user sign‑up controller with email verification and team member addition.
 * This implementation uses in‑memory storage and a stub email sender.
 */
@RestController
@RequestMapping("/api")
public class UserController {

    @Autowired
    private JavaMailSender mailSender;

    // In‑memory user store
    private final Map<String, User> users = new ConcurrentHashMap<>();
    // Token -> email mapping
    private final Map<String, String> verificationTokens = new ConcurrentHashMap<>();

    @PostConstruct
    public void init() {
        // Ensure mailSender is configured; if not, log a warning
        if (mailSender == null) {
            System.err.println("JavaMailSender not configured; email will not be sent.");
        }
    }

    /**
     * Sign‑up endpoint. Accepts email, password, and name.
     * Generates a verification token and sends a confirmation email.
     */
    @PostMapping("/signup")
    public ResponseEntity<String> signup(@RequestBody SignUpRequest request) {
        if (users.containsKey(request.getEmail())) {
            return ResponseEntity.badRequest().body("Email already registered.");
        }

        User user = new User(request.getEmail(), request.getPassword(), request.getName(), false);
        users.put(request.getEmail(), user);

        String token = UUID.randomUUID().toString();
        verificationTokens.put(token, request.getEmail());

        // Send verification email
        sendVerificationEmail(request.getEmail(), token);

        return ResponseEntity.ok("Signup successful. Please check your email to verify your account.");
    }

    /**
     * Email verification endpoint. Activates the user account.
     */
    @GetMapping("/verify")
    public ResponseEntity<String> verify(@RequestParam("token") String token) {
        String email = verificationTokens.remove(token);
        if (email == null) {
            return ResponseEntity.badRequest().body("Invalid or expired verification token.");
        }

        User user = users.get(email);
        if (user == null) {
            return ResponseEntity.badRequest().body("User not found.");
        }

        user.setActive(true);
        return ResponseEntity.ok("Email verified. Your account is now active.");
    }

    /**
     * Add a team member to an existing account.
     * For simplicity, this endpoint just records the member email in the owner's user record.
     */
    @PostMapping("/addTeamMember")
    public ResponseEntity<String> addTeamMember(@RequestBody TeamMemberRequest request) {
        User owner = users.get(request.getOwnerEmail());
        if (owner == null || !owner.isActive()) {
            return ResponseEntity.badRequest().body("Owner account not found or inactive.");
        }

        if (!owner.getTeamMembers().add(request.getMemberEmail())) {
            return ResponseEntity.badRequest().body("Member already added.");
        }

        return ResponseEntity.ok("Team member added successfully.");
    }

    // ---------- Helper Methods & DTOs ----------

    private void sendVerificationEmail(String toEmail, String token) {
        if (mailSender == null) {
            System.out.printf("Mock email to %s: Verify your account using token %s%n", toEmail, token);
            return;
        }

        String verificationLink = "https://example.com/api/verify?token=" + token;
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(toEmail);
        message.setSubject("Verify your Axentx account");
        message.setText("Please verify your account by clicking the following link: " + verificationLink);
        mailSender.send(message);
    }

    // DTOs
    public static class SignUpRequest {
        private String email;
        private String password;
        private String name;

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
    }

    public static class TeamMemberRequest {
        private String ownerEmail;
        private String memberEmail;

        public String getOwnerEmail() { return ownerEmail; }
        public void setOwnerEmail(String ownerEmail) { this.ownerEmail = ownerEmail; }

        public String getMemberEmail() { return memberEmail; }
        public void setMemberEmail(String memberEmail) { this.memberEmail = memberEmail; }
    }

    // Simple User model
    public static class User {
        private final String email;
        private final String password;
        private final String name;
        private boolean active;
        private final Set<String> teamMembers = ConcurrentHashMap.newKeySet();

        public User(String email, String password, String name, boolean active) {
            this.email = email;
            this.password = password;
            this.name = name;
            this.active = active;
        }

        public String getEmail() { return email; }
        public String getPassword() { return password; }
        public String getName() { return name; }
        public boolean isActive() { return active; }
        public void setActive(boolean active) { this.active = active; }
        public Set<String> getTeamMembers() { return teamMembers; }
    }
}