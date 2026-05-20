package com.axentx.surrogate1.client;

import com.axentx.surrogate1.model.CloudResource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.time.LocalDate;
import java.util.Collections;
import java.util.List;

@Component
public class CloudCostApiClient {

    private static final Logger logger = LoggerFactory.getLogger(CloudCostApiClient.class);
    private final WebClient webClient;

    public CloudCostApiClient(@Value("${cloudcost.api.url}") String apiUrl, WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl(apiUrl).build();
    }

    public List<CloudResource> fetchRealTimeResourceUtilization() {
        try {
            logger.info("Fetching real-time resource utilization");
            CloudResource[] resources = webClient.get()
                    .uri("/real-time")
                    .retrieve()
                    .bodyToArray(CloudResource.class);
            return resources != null ? List.of(resources) : Collections.emptyList();
        } catch (WebClientResponseException e) {
            logger.error("Failed to fetch real-time data: {}", e.getMessage());
            throw new CloudCostApiException("Failed to fetch real-time data", e);
        }
    }

    public List<CloudResource> fetchHistoricalResourceUtilization(LocalDate startDate, LocalDate endDate) {
        try {
            logger.info("Fetching historical data from {} to {}", startDate, endDate);
            CloudResource[] resources = webClient.get()
                    .uri(uriBuilder -> uriBuilder
                            .path("/historical")
                            .queryParam("startDate", startDate.toString())
                            .queryParam("endDate", endDate.toString())
                            .build())
                    .retrieve()
                    .bodyToArray(CloudResource.class);
            return resources != null ? List.of(resources) : Collections.emptyList();
        } catch (WebClientResponseException e) {
            logger.error("Failed to fetch historical data: {}", e.getMessage());
            throw new CloudCostApiException("Failed to fetch historical data", e);
        }
    }
}