package com.axentx.rat.service;

import com.axentx.rat.dto.LinkRequest;
import com.axentx.rat.dto.LinkResponse;
import org.springframework.stereotype.Service;

@Service
public class LinkService {

    public LinkResponse initiateLink(LinkRequest linkRequest) {
        // Validate clientId and clientSecret
        if (linkRequest.getClientId() == null || linkRequest.getClientSecret() == null) {
            throw new IllegalArgumentException("Client ID and Secret are required");
        }

        // Generate Plaid link token
        String linkToken = generatePlaidLinkToken(linkRequest);

        // Store link token encrypted at rest
        storeLinkToken(linkToken);

        return new LinkResponse(null, linkToken);
    }

    private String generatePlaidLinkToken(LinkRequest linkRequest) {
        // Logic to generate Plaid link token
        return "sample-link-token";
    }

    private void storeLinkToken(String linkToken) {
        // Logic to store link token encrypted at rest
    }
}