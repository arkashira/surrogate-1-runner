package com.axentx.surrogate1;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/**
 * Simple billing and metering utility.
 *
 * <p>In a real system this class would be replaced by a richer
 * implementation that talks to pricing services, discounts, Knative
 * eventing, etc.  For the purpose of the current feature flag we keep the
 * logic deterministic, pure‑Java and fully unit‑testable.</p>
 */
public final class BillingAndMeteringLogic {

    /** Unit used for the metering data – kept in a constant so the two
     *  output formats never diverge. */
    public static final String USAGE_UNIT = "GB-hours";

    /** CSV format used by {@link #generateMeteringRecord(String,double)}. */
    private static final String CSV_PATTERN = "%s,%d,%.3f";

    private BillingAndMeteringLogic() {
        // static utility – prevent instantiation
    }

    /* --------------------------------------------------------------------- *
     *  Billing
     * --------------------------------------------------------------------- */

    /**
     * Calculates the monetary charge for a given usage amount.
     *
     * @param usage amount of resource used (must be ≥ 0)
     * @param rate  price per unit (must be ≥ 0)
     * @return total charge = {@code usage * rate}
     * @throws IllegalArgumentException if either argument is negative
     */
    public static double calculateCharge(double usage, double rate) {
        if (usage < 0 || rate < 0) {
            throw new IllegalArgumentException("Usage and rate must be non‑negative");
        }
        return usage * rate;
    }

    /* --------------------------------------------------------------------- *
     *  Metering – CSV string
     * --------------------------------------------------------------------- */

    /**
     * Generates a CSV‑style metering record.
     *
     * <pre>
     *   customerId,timestamp,usage
     * </pre>
     *
     * @param customerId non‑null, non‑empty identifier of the customer
     * @param usage      amount of resource used (must be ≥ 0)
     * @return a CSV line that can be written to a file, Kafka topic, etc.
     * @throws IllegalArgumentException if {@code customerId} is blank or {@code usage} is negative
     */
    public static String generateMeteringRecord(String customerId, double usage) {
        validateCustomerId(customerId);
        validateUsage(usage);
        long timestamp = System.currentTimeMillis();
        return String.format(CSV_PATTERN, customerId, timestamp, usage);
    }

    /* --------------------------------------------------------------------- *
     *  Metering – Map representation
     * --------------------------------------------------------------------- */

    /**
     * Returns an immutable map with the same data that the CSV record contains,
     * plus a {@code unit} field.
     *
     * @param customerId non‑null, non‑empty identifier of the customer
     * @param usage      amount of resource used (must be ≥ 0)
     * @return an unmodifiable {@link Map}
     * @throws IllegalArgumentException if {@code customerId} is blank or {@code usage} is negative
     */
    public static Map<String, Object> getMeteringData(String customerId, double usage) {
        validateCustomerId(customerId);
        validateUsage(usage);
        long timestamp = System.currentTimeMillis();

        Map<String, Object> data = new HashMap<>();
        data.put("customerId", customerId);
        data.put("usage", usage);
        data.put("timestamp", timestamp);
        data.put("unit", USAGE_UNIT);
        return Collections.unmodifiableMap(data);
    }

    /* --------------------------------------------------------------------- *
     *  Validation helpers (package‑private for test visibility)
     * --------------------------------------------------------------------- */

    static void validateCustomerId(String customerId) {
        if (customerId == null || customerId.isBlank()) {
            throw new IllegalArgumentException("Customer ID must be provided and non‑blank");
        }
    }

    static void validateUsage(double usage) {
        if (usage < 0) {
            throw new IllegalArgumentException("Usage must be non‑negative");
        }
    }
}