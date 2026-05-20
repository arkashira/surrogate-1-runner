package com.axentx.surrogate1;

import software.amazon.awssdk.services.cloudtrail.CloudTrailClient;
import software.amazon.awssdk.services.cloudtrail.model.LookupEventsRequest;
import software.amazon.awssdk.services.cloudtrail.model.LookupEventsResponse;

import java.time.Instant;
import java.util.List;

public class LogCollector {
    private final CloudTrailClient cloudTrailClient;

    public LogCollector(CloudTrailClient cloudTrailClient) {
        this.cloudTrailClient = cloudTrailClient;
    }

    public List<LookupEventsResponse> getPrivilegedAccountActivityLogs(Instant startTime, Instant endTime) {
        LookupEventsRequest request = LookupEventsRequest.builder()
                .startTime(startTime.toString())
                .endTime(endTime.toString())
                .eventTypeList(List.of("AWS API Call via CloudTrail")) // replace with actual event types
                .build();

        return cloudTrailClient.lookupEventsPaginator(request).collectList().join();
    }
}