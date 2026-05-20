package com.axentx.surrogate1.controllers;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BillingController {

    @PostMapping("/update_billing_info")
    public String updateBillingInfo(@RequestParam("card_number") String cardNumber, @RequestParam("expiration_date") String expirationDate) {
        // Logic to update billing information
        return "Billing information updated";
    }
}