package com.axentx.surrogate1.controller;

import com.axentx.surrogate1.service.UserService;
import com.axentx.surrogate1.service.EmailService;
import com.axentx.surrogate1.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponentsBuilder;

import javax.validation.Valid;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import java.net.URI;

/**
 * REST controller responsible for user registration.
 *
 * <p>Endpoint: {@code POST /api/users/register}
 *
 * <p>Accepts an email and password, creates a new user, sends a confirmation email,
 * and redirects the client to the dashboard upon successful registration.
 */
@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private EmailService emailService;

    /**
     * Registers a new user.
     *
     * @param request the registration request payload
     * @param uriBuilder utility to build the redirect URI
     * @return HTTP 302 redirect to the dashboard
     */
    @PostMapping("/register")
    public ResponseEntity<Void> register(
            @Valid @RequestBody RegisterRequest request,
            UriComponentsBuilder uriBuilder) {

        // Create the user via the service layer
        User user = userService.registerUser(request.getEmail(), request.getPassword());

        // Send a confirmation email
        emailService.sendConfirmationEmail(user);

        // Redirect to the dashboard
        URI dashboardUri = uriBuilder.path("/dashboard").build().toUri();
        return ResponseEntity.status(HttpStatus.FOUND).location(dashboardUri).build();
    }

    /**
     * DTO for registration requests.
     */
    public static class RegisterRequest {

        @NotBlank(message = "Email must not be blank")
        @Email(message = "Email should be valid")
        private String email;

        @NotBlank(message = "Password must not be blank")
        private String password;

        public RegisterRequest() {
        }

        public RegisterRequest(String email, String password) {
            this.email = email;
            this.password = password;
        }

        public String getEmail() {
            return email;
        }

        public void setEmail(String email) {
            this.email = email;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }
    }
}