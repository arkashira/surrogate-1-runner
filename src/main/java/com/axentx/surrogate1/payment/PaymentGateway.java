package com.axentx.surrogate1.payment;

import java.util.Map;

public class PaymentGateway {
    private String apiKey;
    private String apiSecret;

    public PaymentGateway(String apiKey, String apiSecret) {
        this.apiKey = apiKey;
        this.apiSecret = apiSecret;
    }

    public boolean processPayment(Map<String, Object> invoiceDetails) {
        // Simulate payment processing logic here
        // In a real scenario, this method would interact with a payment gateway API
        System.out.println("Processing payment for invoice: " + invoiceDetails.get("invoiceId"));
        return true; // Return true if payment is successful, false otherwise
    }
}