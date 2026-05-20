package dashboard;

import java.util.List;

/**
 * Simple interface for the validation engine.
 * Implementations should perform validation on the given collection
 * and return a list of human‑readable issue messages.
 */
public interface ValidationEngine {
    List<String> validate(String collectionId);
}