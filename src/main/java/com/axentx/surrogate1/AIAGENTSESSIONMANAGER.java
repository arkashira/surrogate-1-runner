
package com.axentx.surrogate1;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.client.RestTemplate;
import com.google.cloud.pubsub.v1.Publisher;
import com.google.cloud.pubsub.v1.PubsubMessage;

@Service
public class AIAGENTSESSIONMANAGER {

    @Value("${cloud.pubsub.topic}")
    private String pubsubTopic;

    private final RestTemplate restTemplate = new RestTemplate();
    private final Publisher<String> pubsubPublisher;

    public AIAGENTSESSIONMANAGER(Publisher<String> pubsubPublisher) {
        this.pubsubPublisher = pubsubPublisher;
    }

    @Scheduled(fixedRate = 300000) // 300000 ms = 5 minutes
    public void checkScaling() {
        String scalingUrl = "https://my-scaling-service.com/api/scale";
        String response = restTemplate.getForObject(scalingUrl, String.class);
        if (response.equals("scaleUp")) {
            String message = "{\"action\": \"scaleUp\"}";
            publishToPubsub(message);
        } else if (response.equals("scaleDown")) {
            String message = "{\"action\": \"scaleDown\"}";
            publishToPubsub(message);
        }
    }

    private void publishToPubsub(String message) {
        PubsubMessage pubsubMessage = PubsubMessage.newBuilder()
                .setData(message)
                .build();
        pubsubPublisher.publish(pubsubTopic, pubsubMessage);
    }
}