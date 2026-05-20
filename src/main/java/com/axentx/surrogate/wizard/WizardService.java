package com.axentx.surrogate.wizard;

import com.github.jcanton.cron4j.CronExpression;
import com.github.jcanton.cron4j.CronParser;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public class WizardService {

    /**
     * Validates a cron expression using Cron4j library.
     * Returns a validation result indicating if the expression is valid and any error message.
     */
    public ValidationResult validateCron(String cronExpression) {
        try {
            CronParser parser = new CronParser(cronExpression);
            parser.parse();
            return new ValidationResult(true, "Valid cron expression");
        } catch (Exception e) {
            return new ValidationResult(false, "Invalid cron expression: " + e.getMessage());
        }
    }

    /**
     * Calculates the next valid execution time for a given cron expression.
     * Returns the next scheduled run time as a ZonedDateTime.
     */
    public ZonedDateTime getNextRunTime(String cronExpression, long now) {
        try {
            CronExpression expr = new CronExpression(cronExpression);
            return expr.getNextValidTimeAfter(ZonedDateTime.now());
        } catch (Exception e) {
            throw new RuntimeException("Failed to parse cron expression", e);
        }
    }

    /**
     * Represents the result of cron validation.
     */
    public static class ValidationResult {
        private final boolean valid;
        private final String message;

        public ValidationResult(boolean valid, String message) {
            this.valid = valid;
            this.message = message;
        }

        public boolean isValid() {
            return valid;
        }

        public String getMessage() {
            return message;
        }
    }
}