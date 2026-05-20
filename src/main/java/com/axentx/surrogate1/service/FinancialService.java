package com.axentx.surrogate1.service;

import com.axentx.surrogate1.model.Transaction;
import com.axentx.surrogate1.repository.TransactionRepository;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Service responsible for calculating the Profit & Loss (P&L) summary.
 *
 * <p>
 *   - Calculates P&L from the last 30 days of {@link Transaction} data.
 *   - Caches the result and refreshes it automatically every 24 hours.
 *   - Provides a {@code refreshNow()} method that can be called by other
 *     components when new data is imported, ensuring real‑time updates.
 *   - Exposes helpers for formatted output and colour coding.
 * </p>
 */
@Service
public class FinancialService {

    private final TransactionRepository transactionRepository;
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();

    // Cached values – volatile for safe publication across threads
    private volatile BigDecimal cachedPnL = BigDecimal.ZERO;
    private volatile Instant lastRefresh = Instant.EPOCH;

    public FinancialService(TransactionRepository transactionRepository) {
        this.transactionRepository = transactionRepository;
    }

    /**
     * Initialise the periodic refresh task after bean construction.
     */
    @PostConstruct
    private void initRefreshTask() {
        // Refresh immediately, then every 24 hours
        scheduler.scheduleAtFixedRate(this::refreshCache, 0, 24, TimeUnit.HOURS);
    }

    /**
     * Re‑calculate the P&L for the last 30 days and update the cache.
     */
    private void refreshCache() {
        cachedPnL = calculatePnL();
        lastRefresh = Instant.now();
    }

    /**
     * Public entry point to force an immediate refresh (e.g., after new data import).
     */
    public void refreshNow() {
        refreshCache();
    }

    /**
     * Returns the most recent cached P&L value.
     *
     * @return profit (positive) or loss (negative) as {@link BigDecimal}
     */
    public BigDecimal getCurrentPnL() {
        return cachedPnL;
    }

    /**
     * Returns a colour code based on the current P&L.
     *
     * @return "green" for profit or zero, "red" for loss
     */
    public String getPnLColor() {
        return cachedPnL.compareTo(BigDecimal.ZERO) >= 0 ? "green" : "red";
    }

    /**
     * Returns a human‑readable, dollar‑formatted representation of the current P&L.
     *
     * @return string like "$1234.56"
     */
    public String getPnLFormatted() {
        return "$" + cachedPnL.setScale(2, RoundingMode.HALF_UP).toString();
    }

    /**
     * Core calculation: sum of transaction amounts from the last 30 days.
     *
     * @return total profit (positive) or loss (negative)
     */
    private BigDecimal calculatePnL() {
        Instant thirtyDaysAgo = Instant.now().minus(30, ChronoUnit.DAYS);
        List<Transaction> recentTx = transactionRepository.findByTimestampAfter(thirtyDaysAgo);
        return recentTx.stream()
                .map(Transaction::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}