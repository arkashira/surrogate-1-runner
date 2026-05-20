
package com.axentx.surrogate1.service;

import com.axentx.surrogate1.UserProfile;
import com.axentx.surrogate1.repository.UserProfileRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserProfileService {
    @Autowired
    private UserProfileRepository userProfileRepository;

    public UserProfile createUserProfile(String username, String password, String firstName, String lastName) {
        UserProfile userProfile = new UserProfile();
        userProfile.setUsername(username);
        userProfile.setPassword(password);
        userProfile.setFirstName(firstName);
        userProfile.setLastName(lastName);
        userProfile.setCreatedAt(new Date());
        userProfile.setUpdatedAt(new Date());
        return userProfileRepository.save(userProfile);
    }

    // other methods for login, edit profile, etc.
}