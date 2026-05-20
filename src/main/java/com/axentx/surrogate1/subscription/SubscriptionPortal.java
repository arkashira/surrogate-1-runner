package com.axentx.surrogate1.subscription;

import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class SubscriptionPortal {

    private static final String ALGORITHM = "AES/CBC/PKCS5Padding";
    private static final int KEY_SIZE = 128;
    private static final SecureRandom random = new SecureRandom();

    public void displaySubscriptionPortal() {
        System.out.println("Welcome to the Premium Firmware Service Subscription Portal!");
        System.out.println("Please follow the steps to subscribe and unlock advanced features.");
        // Here you can add UI elements to make it user-friendly
    }

    public boolean processSubscription(String userId, String paymentInfo) {
        try {
            // Simulate secure payment processing
            String encryptedPaymentInfo = encryptData(paymentInfo);
            // Simulate database interaction to save subscription details
            saveSubscriptionDetails(userId, encryptedPaymentInfo);
            return true; // Subscription successful
        } catch (Exception e) {
            e.printStackTrace();
            return false; // Subscription failed
        }
    }

    private String encryptData(String data) throws Exception {
        byte[] keyBytes = new byte[KEY_SIZE / 8];
        random.nextBytes(keyBytes);
        SecretKeySpec keySpec = new SecretKeySpec(keyBytes, "AES");

        byte[] iv = new byte[Cipher.BLOCK_SIZE];
        random.nextBytes(iv);
        IvParameterSpec ivSpec = new IvParameterSpec(iv);

        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, ivSpec);

        byte[] encrypted = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encrypted);
    }

    private void saveSubscriptionDetails(String userId, String encryptedPaymentInfo) {
        // Simulate saving subscription details to a secure database
        System.out.println("Subscription details saved for user: " + userId);
    }
}