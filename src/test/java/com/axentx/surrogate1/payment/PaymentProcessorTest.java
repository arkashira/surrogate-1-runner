package com.axentx.surrogate1.payment;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class PaymentProcessorTest {

    @Mock
    private PaymentProcessor paymentProcessor;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCreateCustomer() {
        String customerId = "cus_123";
        when(paymentProcessor.createCustomer("test@example.com", "Test User")).thenReturn(customerId);

        String result = paymentProcessor.createCustomer("test@example.com", "Test User");
        assertEquals(customerId, result);
    }

    @Test
    void testChargeCustomer() {
        String chargeId = "ch_123";
        when(paymentProcessor.chargeCustomer("cus_123", 10.0, "Test Charge")).thenReturn(chargeId);

        String result = paymentProcessor.chargeCustomer("cus_123", 10.0, "Test Charge");
        assertEquals(chargeId, result);
    }

    @Test
    void testVerifyPayment() {
        when(paymentProcessor.verifyPayment("ch_123")).thenReturn(true);

        boolean result = paymentProcessor.verifyPayment("ch_123");
        assertTrue(result);
    }
}