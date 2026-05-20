package api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/validation")
public class ValidationApi {

    @PostMapping("/scan")
    public String triggerValidationScan(@RequestBody ValidationRequest request) {
        // Logic to trigger validation scan using the provided request data
        return "Validation scan triggered for collection: " + request.getCollectionId();
    }

    @GetMapping("/results")
    public String getValidationResults() {
        // Logic to fetch and display validation results
        return "Validation results for the latest scan.";
    }

    static class ValidationRequest {
        private String collectionId;

        public String getCollectionId() {
            return collectionId;
        }

        public void setCollectionId(String collectionId) {
            this.collectionId = collectionId;
        }
    }
}