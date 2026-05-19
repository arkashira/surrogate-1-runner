package com.axentx.younginvestor;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Generates an age‑appropriate investment roadmap for a user.
 *
 * <p>The roadmap is a numbered list of actionable steps.  It is
 * parameterised by the user’s age and risk profile so that the
 * recommendations can be customised for different investment styles.</p>
 *
 * <p>All public methods are thread‑safe and the class has no mutable state.</p>
 */
public final class InvestmentRoadmapGenerator {

    /** Supported risk profiles. */
    public enum Profile {
        CONSERVATIVE,
        MODERATE,
        AGGRESSIVE
    }

    /** Private constructor – this is a utility class. */
    private InvestmentRoadmapGenerator() {
    }

    /**
     * Generates a roadmap based on the provided age and risk profile.
     *
     * @param age     the user’s age in years (must be ≥ 0)
     * @param profile the user’s risk profile; if {@code null} defaults to {@link Profile#MODERATE}
     * @return an immutable list of numbered roadmap steps
     * @throws IllegalArgumentException if {@code age < 0}
     */
    public static List<String> generateRoadmap(int age, Profile profile) {
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }

        Profile effectiveProfile = (profile == null) ? Profile.MODERATE : profile;

        List<String> steps = new ArrayList<>();

        // Age brackets – the same ranges that were used in both candidates
        if (age < 18) {
            steps.add("1. Focus on education and saving for the future.");
            return Collections.unmodifiableList(steps);
        }

        if (age <= 25) {
            steps.add("1. Build an emergency fund covering 3–6 months of expenses.");
            steps.add("2. Start contributing to a retirement account (e.g., 401(k), IRA).");
            steps.add("3. Invest in low‑cost index funds or ETFs for long‑term growth.");
        } else if (age <= 35) {
            steps.add("1. Max out retirement contributions and maintain the emergency fund.");
            steps.add("2. Diversify the portfolio with a mix of equities, bonds, and alternative assets.");
            steps.add("3. Review risk tolerance and adjust asset allocation accordingly.");
        } else if (age <= 50) {
            steps.add("1. Maintain a diversified portfolio with a balanced risk profile.");
            steps.add("2. Increase retirement contributions as you approach retirement.");
            steps.add("3. Consider tax‑advantaged accounts and estate planning.");
        } else { // age > 50
            steps.add("1. Focus on preserving capital and generating income.");
            steps.add("2. Rebalance the portfolio to a more conservative allocation.");
            steps.add("3. Plan for estate transfer and legacy goals.");
        }

        // Profile‑specific advice – the same logic as Candidate 1
        switch (effectiveProfile) {
            case CONSERVATIVE:
                steps.add("4. Prioritize bonds and dividend‑paying stocks.");
                break;
            case MODERATE:
                steps.add("4. Maintain a balanced mix of equities and bonds.");
                break;
            case AGGRESSIVE:
                steps.add("4. Allocate a higher percentage to equities and growth sectors.");
                break;
        }

        return Collections.unmodifiableList(steps);
    }
}