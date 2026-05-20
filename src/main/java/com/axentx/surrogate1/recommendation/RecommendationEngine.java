// ────────────────────────────────────────────────────────────────────────────────
//  Recommendation.java
// ────────────────────────────────────────────────────────────────────────────────
package com.axentx.surrogate1.recommendation;

import java.util.Objects;

/**
 * Immutable POJO representing a cost‑saving recommendation.
 *
 * <p>Implements {@link Comparable} so that a list of {@code Recommendation}
 * instances can be sorted by {@code potentialSavingsUsd} in descending order.</p>
 */
public final class Recommendation implements Comparable<Recommendation> {
    private final String resourceId;
    private final String description;
    private final double potentialSavingsUsd;

    public Recommendation(String resourceId, String description, double potentialSavingsUsd) {
        this.resourceId = Objects.requireNonNull(resourceId, "resourceId");
        this.description = Objects.requireNonNull(description, "description");
        this.potentialSavingsUsd = potentialSavingsUsd;
    }

    public String getResourceId() {
        return resourceId;
    }

    public String getDescription() {
        return description;
    }

    public double getPotentialSavingsUsd() {
        return potentialSavingsUsd;
    }

    @Override
    public int compareTo(Recommendation other) {
        // descending order
        return Double.compare(other.potentialSavingsUsd, this.potentialSavingsUsd);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Recommendation that)) return false;
        return Double.compare(that.potentialSavingsUsd, potentialSavingsUsd) == 0 &&
               resourceId.equals(that.resourceId) &&
               description.equals(that.description);
    }

    @Override
    public int hashCode() {
        return Objects.hash(resourceId, description, potentialSavingsUsd);
    }

    @Override
    public String toString() {
        return String.format(
                "Recommendation{resourceId='%s', description='%s', potentialSavingsUsd=%.2f}",
                resourceId, description, potentialSavingsUsd);
    }
}