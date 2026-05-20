package dashboard;

import org.springframework.stereotype.Service;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ValidationEngineService {

    private final ValidationEngine validationEngine;
    private final Map<String, ValidationResult> results = new ConcurrentHashMap<>();

    public ValidationEngineService(ValidationEngine validationEngine) {
        this.validationEngine = validationEngine;
    }

    /**
     * Run validation for a single collection and store the result.
     */
    public ValidationResult runValidation(String collectionId) {
        List<String> issues = validationEngine.validate(collectionId);
        ValidationResult result = new ValidationResult(
                collectionId,
                issues.isEmpty() ? "PASS" : "FAIL",
                issues
        );
        results.put(collectionId, result);
        return result;
    }

    public Optional<ValidationResult> getResult(String collectionId) {
        return Optional.ofNullable(results.get(collectionId));
    }

    public Collection<ValidationResult> getAllResults() {
        return results.values();
    }
}