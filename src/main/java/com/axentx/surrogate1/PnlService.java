package com.axentx.surrogate1;

import com.axentx.surrogate1.model.PnlData;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

/**
 * Service responsible for fetching and caching Profit & Loss data.
 * <p>
 * The service periodically refreshes its cache (default every 5 seconds) to
 * provide near‑real‑time data to the dashboard. In case of a fetch failure,
 * the previously cached data is retained.
 */
@Service
public class PnlService {

    private static final String PNL_ENDPOINT = "https://api.example.com/pnl";

    private final RestTemplate restTemplate;

    /** Holds the most recent P&L snapshot. Volatile for safe publication across threads. */
    private volatile PnlData cachedData = new PnlData(0.0, 0.0, 0.0);

    public PnlService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    /**
     * Returns the latest cached Profit & Loss data.
     *
     * @return current {@link PnlData}
     */
    public PnlData getCurrentData() {
        return cachedData;
    }

    /**
     * Refreshes the cached data by calling the external P&L endpoint.
     * Runs automatically according to the schedule defined below.
     */
    @Scheduled(fixedRateString = "${pnl.refresh.rate.ms:5000}")
    public void refreshCache() {
        PnlData fresh = fetchFromEndpoint();
        if (fresh != null) {
            cachedData = fresh;
        }
    }

    /**
     * Performs the actual HTTP request to retrieve P&L data.
     *
     * @return {@link PnlData} on success, {@code null} on failure.
     */
    private PnlData fetchFromEndpoint() {
        try {
            return restTemplate.getForObject(PNL_ENDPOINT, PnlData.class);
        } catch (Exception ex) {
            // Log the exception in a real system; omitted here for brevity.
            return null;
        }
    }
}