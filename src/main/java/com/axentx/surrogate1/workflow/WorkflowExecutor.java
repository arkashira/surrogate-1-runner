package com.axentx.surrogate1.workflow;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.Map;
import java.util.HashMap;

public class WorkflowExecutor {
    private static final Logger logger = LoggerFactory.getLogger(WorkflowExecutor.class);
    private final ExecutorService executor;
    private final Map<String, Future<?>> runningTasks = new ConcurrentHashMap<>();
    private final AtomicInteger activeTasks = new AtomicInteger(0);
    private static final int MAX_PARALLEL_TASKS = Runtime.getRuntime().availableProcessors() * 2;

    public WorkflowExecutor() {
        this.executor = Executors.newFixedThreadPool(MAX_PARALLEL_TASKS,
            new ThreadFactory() {
                private final AtomicInteger counter = new AtomicInteger(0);
                
                @Override
                public Thread newThread(Runnable r) {
                    Thread t = new Thread(r, "workflow-executor-" + counter.incrementAndGet());
                    t.setDaemon(true);
                    return t;
                }
            });
    }

    public void executeWorkflow(String workflowId, Runnable task) {
        if (activeTasks.get() >= MAX_PARALLEL_TASKS) {
            throw new WorkflowException("Maximum parallel tasks (" + MAX_PARALLEL_TASKS + ") reached");
        }

        activeTasks.incrementAndGet();
        Future<?> future = executor.submit(() -> {
            try {
                long startTime = System.currentTimeMillis();
                task.run();
                long duration = System.currentTimeMillis() - startTime;
                logger.info("Workflow {} completed in {} ms", workflowId, duration);
            } catch (Exception e) {
                logger.error("Workflow {} failed: {}", workflowId, e.getMessage(), e);
                throw new WorkflowException("Workflow execution failed: " + e.getMessage(), e);
            } finally {
                runningTasks.remove(workflowId);
                activeTasks.decrementAndGet();
            }
        });
        
        runningTasks.put(workflowId, future);
    }

    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }

    public Map<String, Object> getMetrics() {
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("activeTasks", activeTasks.get());
        metrics.put("maxParallelTasks", MAX_PARALLEL_TASKS);
        metrics.put("queueSize", ((ThreadPoolExecutor) executor).getQueue().size());
        return metrics;
    }

    public static class WorkflowException extends RuntimeException {
        public WorkflowException(String message) {
            super(message);
        }

        public WorkflowException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}