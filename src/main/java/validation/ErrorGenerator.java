package validation;

import java.util.List;
import java.util.Map;

public class ErrorGenerator {

    private static final String COLLECTION_ISSUE_TEMPLATE = "Issue found in collection %s: %s";

    /**
     * Generates an error message based on the identified issue.
     *
     * @param collectionName The name of the collection where the issue was found.
     * @param issueDetails   Details about the issue.
     * @return A formatted error message.
     */
    public static String generateErrorMessage(String collectionName, String issueDetails) {
        return String.format(COLLECTION_ISSUE_TEMPLATE, collectionName, issueDetails);
    }

    /**
     * Generates a list of error messages for multiple issues.
     *
     * @param issues A map containing collection names and their respective issue details.
     * @return A list of formatted error messages.
     */
    public static List<String> generateErrorMessages(Map<String, String> issues) {
        return issues.entrySet().stream()
                .map(entry -> generateErrorMessage(entry.getKey(), entry.getValue()))
                .toList();
    }
}