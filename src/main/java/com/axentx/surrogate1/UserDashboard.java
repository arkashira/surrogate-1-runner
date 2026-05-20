package com.axentx.surrogate1;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class UserDashboard {

    @GetMapping("/dashboard")
    public String showDashboard(Model model) {
        // Fetch user data and recorded streams
        String username = "currentUsername"; // Replace with actual user retrieval logic
        model.addAttribute("username", username);
        model.addAttribute("recordedStreams", getRecordedStreams(username));
        return "dashboard";
    }

    @PostMapping("/login")
    public String login(@RequestParam String username, @RequestParam String password, Model model) {
        // Implement login logic here
        if (isValidLogin(username, password)) {
            model.addAttribute("username", username);
            return "redirect:/dashboard";
        } else {
            model.addAttribute("error", "Invalid credentials");
            return "login";
        }
    }

    private boolean isValidLogin(String username, String password) {
        // Replace with actual authentication logic
        return "testUser".equals(username) && "testPassword".equals(password);
    }

    private Object[] getRecordedStreams(String username) {
        // Replace with actual stream retrieval logic
        return new Object[]{"Stream1", "Stream2"};
    }
}