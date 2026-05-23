package com.axentx.surrogate.service;

import com.axentx.surrogate.model.BillingInformation;
import com.axentx.surrogate.repository.BillingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;
import java.util.Base64;

@Service
public class BillingService {

    private static final String ALGORITHM = "AES";
    private static final String SECRET_KEY = "your-secret-key"; // Replace with your secret key

    @Autowired
    private BillingRepository billingRepository;

    public BillingInformation saveBillingInformation(BillingInformation billingInformation) {
        try {
            String encryptedCardNumber = encrypt(billingInformation.getCardNumber());
            billingInformation.setCardNumber(encryptedCardNumber);
            return billingRepository.save(billingInformation);
        } catch (Exception e) {
            throw new RuntimeException("Failed to save billing information", e);
        }
    }

    public BillingInformation getBillingInformation(Long id) {
        BillingInformation billingInformation = billingRepository.findById(id).orElse(null);
        if (billingInformation != null) {
            try {
                String decryptedCardNumber = decrypt(billingInformation.getCardNumber());
                billingInformation.setCardNumber(decryptedCardNumber);
            } catch (Exception e) {
                throw new RuntimeException("Failed to retrieve billing information", e);
            }
        }
        return billingInformation;
    }

    private String encrypt(String data) throws Exception {
        Key key = generateKey();
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encryptedBytes = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    private String decrypt(String encryptedData) throws Exception {
        Key key = generateKey();
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] decodedBytes = Base64.getDecoder().decode(encryptedData);
        byte[] decryptedBytes = cipher.doFinal(decodedBytes);
        return new String(decryptedBytes);
    }

    private Key generateKey() throws Exception {
        return new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
    }
}