package com.axentx.surrogate1.controllers;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SubscriptionController {

    @PostMapping("/update_subscription")
    public String updateSubscription(@RequestParam("plan") String plan) {
        // Logic to update subscription plan
        return "Subscription updated to " + plan;
    }
}