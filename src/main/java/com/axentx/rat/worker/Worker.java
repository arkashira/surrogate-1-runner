package com.axentx.rat.worker;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.stereotype.Component;

@Component
public class Worker {

    private final Counter workerSuccessCounter;
    private final MeterRegistry meterRegistry;

    public Worker(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.workerSuccessCounter = Counter.builder("rat_worker_success_total")
                .tag("worker", "default")
                .register(meterRegistry);
    }

    public void doWork() {
        // Existing worker logic here
        workerSuccessCounter.increment();
    }
}