package com.axentx.surrogate1.setup;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * A very small in‑memory setup service that walks a user through a
 * four‑step guided setup process.  Each step is exposed via a REST
 * endpoint and the client can poll for progress.  This is intentionally
 * lightweight – it is only used for the demo UI in /static/setup.js.
 */
@RestController
@RequestMapping("/api/setup")
public class SetupService {

    /**
     * The steps of the guided setup.  The order is important.
     */
    private enum Step {
        VERIFY_ENV("Verify environment"),
        INSTALL_DEPS("Install dependencies"),
        CONFIGURE("Configure application"),
        FINALIZE("Finalize setup");

        private final String description;

        Step(String description) {
            this.description = description;
        }

        public String getDescription() {
            return description;
        }
    }

    // Current step index (0‑based).  In a real system this would be persisted per user.
    private final AtomicInteger currentStep = new AtomicInteger(0);

    /**
     * Returns the current status of the setup process.
     *
     * @return a JSON object containing the current step number, description,
     *         and whether the process is complete.
     */
    @GetMapping("/status")
    public ResponseEntity<SetupStatus> status() {
        int stepIndex = currentStep.get();
        boolean complete = stepIndex >= Step.values().length;
        SetupStatus status = new SetupStatus(
                complete ? -1 : stepIndex,
                complete ? "Setup complete" : Step.values()[stepIndex].getDescription(),
                complete
        );
        return ResponseEntity.ok(status);
    }

    /**
     * Advances the setup to the next step.  In a real implementation each
     * step would perform real work; here we simply simulate a delay.
     *
     * @return the new status after advancing.
     */
    @PostMapping("/next")
    public ResponseEntity<SetupStatus> next() {
        int stepIndex = currentStep.getAndIncrement();
        // Simulate work with a short sleep – in production this would be
        // actual logic such as checking env vars, installing packages, etc.
        try {
            Thread.sleep(500); // 0.5s per step
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        int newIndex = currentStep.get();
        boolean complete = newIndex >= Step.values().length;
        SetupStatus status = new SetupStatus(
                complete ? -1 : newIndex,
                complete ? "Setup complete" : Step.values()[newIndex].getDescription(),
                complete
        );
        return ResponseEntity.ok(status);
    }

    /**
     * Simple DTO for JSON responses.
     */
    public record SetupStatus(int step, String message, boolean complete) {}
}