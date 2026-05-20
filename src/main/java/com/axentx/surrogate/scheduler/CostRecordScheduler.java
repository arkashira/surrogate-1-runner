package com.axentx.surrogate.scheduler;

import com.axentx.surrogate.service.CostRecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class CostRecordScheduler {

    @Autowired private CostRecordService service;

    /** Cache the result every midnight – the API can return it instantly. */
    @Scheduled(cron = "0 0 0 * * ?")
    public void refreshTopCostDriversCache() {
        service.getTopCostDrivers(); // side‑effect: can be wired to a cache
    }
}