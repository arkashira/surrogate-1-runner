package com.axentx.surrogate1.payment;

import com.stripe.Stripe;
import com.stripe.model.Charge;
import com.stripe.model.Customer;
import com.stripe.net.APIResource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class PaymentProcessor {

    @Value("${stripe.secret.key}")
    private String stripeSecretKey;

    public void initialize() {
        Stripe.apiKey = stripeSecretKey;
    }

    public String createCustomer(String email, String name) {
        Map<String, Object> customerParams = new HashMap<>();
        customerParams.put("email", email);
        customerParams.put("name", name);
        return Customer.create(customerParams).getId();
    }

    public String chargeCustomer(String customerId, double amount, String description) {
        Map<String, Object> chargeParams = new HashMap<>();
        chargeParams.put("amount", (int) (amount * 100)); // amount in cents
        chargeParams.put("currency", "usd");
        chargeParams.put("customer", customerId);
        chargeParams.put("description", description);
        return Charge.create(chargeParams).getId();
    }

    public boolean verifyPayment(String chargeId) {
        try {
            Charge charge = Charge.retrieve(chargeId);
            return charge.getPaid();
        } catch (Exception e) {
            return false;
        }
    }
}