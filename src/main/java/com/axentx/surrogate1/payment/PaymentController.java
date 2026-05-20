package com.axentx.surrogate1.payment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/payment")
public class PaymentController {

    @Autowired
    private PaymentProcessor paymentProcessor;

    @PostMapping("/create-customer")
    public String createCustomer(@RequestParam String email, @RequestParam String name) {
        return paymentProcessor.createCustomer(email, name);
    }

    @PostMapping("/charge-customer")
    public String chargeCustomer(@RequestParam String customerId, @RequestParam double amount, @RequestParam String description) {
        return paymentProcessor.chargeCustomer(customerId, amount, description);
    }

    @GetMapping("/verify-payment")
    public boolean verifyPayment(@RequestParam String chargeId) {
        return paymentProcessor.verifyPayment(chargeId);
    }
}