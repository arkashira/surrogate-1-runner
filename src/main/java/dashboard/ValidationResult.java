package dashboard;

import java.util.List;

public class ValidationResult {
    private String collectionId;
    private String status;
    private List<String> issues;

    public ValidationResult(String collectionId, String status, List<String> issues) {
        this.collectionId = collectionId;
        this.status = status;
        this.issues = issues;
    }

    public String getCollectionId() {
        return collectionId;
    }

    public void setCollectionId(String collectionId) {
        this.collectionId = collectionId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public List<String> getIssues() {
        return issues;
    }

    public void setIssues(List<String> issues) {
        this.issues = issues;
    }
}