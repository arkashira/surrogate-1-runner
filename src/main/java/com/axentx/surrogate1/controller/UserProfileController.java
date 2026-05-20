
package com.axentx.surrogate1.controller;

import com.axentx.surrogate1.UserProfile;
import com.axentx.surrogate1.service.UserProfileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/user-profile")
public class UserProfileController {
    @Autowired
    private UserProfileService userProfileService;

    @PostMapping("/create")
    public UserProfile createUserProfile(@RequestBody UserProfile userProfile) {
        return userProfileService.createUserProfile(userProfile.getUsername(), userProfile.getPassword(), userProfile.getFirstName(), userProfile.getLastName());
    }

    // other endpoints for login, edit profile, etc.
}