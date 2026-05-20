package com.axentx.surrogate1.controllers;

import com.axentx.surrogate1.dto.ProfileRequest;
import com.axentx.surrogate1.services.ProfileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@RestController
@RequestMapping("/api/profile")
public class ProfileController {

    @Autowired
    private ProfileService profileService;

    @PostMapping
    public ResponseEntity<?> createProfile(@Valid @RequestBody ProfileRequest request, BindingResult result) {
        if (result.hasErrors()) {
            return ResponseEntity.badRequest().body(result.getAllErrors());
        }
        profileService.saveProfile(request);
        return ResponseEntity.ok("Profile created successfully");
    }

    @ExceptionHandler
    public ResponseEntity<?> handleValidationExceptions(Exception ex) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid input data: " + ex.getMessage());
    }
}