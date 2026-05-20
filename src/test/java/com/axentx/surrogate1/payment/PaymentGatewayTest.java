package com.axentx.surrogate1.payment;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class PaymentGatewayTest {
    @Test
    public void testProcessPayment() {
        PaymentGateway paymentGateway = new PaymentGateway("testApiKey", "testApiSecret");
        Map<String, Object> invoiceDetails = new HashMap<>();
        invoiceDetails.put("invoiceId", "INV123");

        boolean result = paymentGateway.processPayment(invoiceDetails);
        assertTrue(result, "Payment should be processed successfully");
    }
}