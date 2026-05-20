package com.axentx.surrogate1.performance;

import com.axentx.surrogate1.hardware.HardwareDetector;
import com.axentx.surrogate1.workload.WorkloadExecutor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Component
public class PerformanceOptimizer {

    private static final Logger logger = LoggerFactory.getLogger(PerformanceOptimizer.class);

    private final HardwareDetector hardwareDetector;
    private final WorkloadExecutor workloadExecutor;
    private final ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();

    public PerformanceOptimizer(HardwareDetector hardwareDetector, WorkloadExecutor workloadExecutor) {
        this.hardwareDetector = hardwareDetector;
        this.workloadExecutor = workloadExecutor;
    }

    @PostConstruct
    public void init() {
        logger.info("Initializing PerformanceOptimizer");
        executor.scheduleAtFixedRate(this::optimizeWorkload, 0, 30, TimeUnit.MINUTES);
    }

    private void optimizeWorkload() {
        logger.info("Optimizing workload...");
        String hardwareConfig = hardwareDetector.detectHardwareConfiguration();
        workloadExecutor.executeWorkloadWithOptimization(hardwareConfig);
        logger.info("Workload optimization completed.");
    }
}