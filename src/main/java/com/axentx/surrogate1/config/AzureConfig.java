package com.axentx.surrogate1.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AzureConfig {

    @Value("${azure.client.id}")
    private String clientId;

    @Value("${azure.client.secret}")
    private String clientSecret;

    @Value("${azure.tenant.id}")
    private String tenantId;

    @Value("${azure.subscription.id}")
    private String subscriptionId;

    public String getClientId() {
        return clientId;
    }

    public String getClientSecret() {
        return clientSecret;
    }

    public String getTenantId() {
        return tenantId;
    }

    public String getSubscriptionId() {
        return subscriptionId;
    }
}