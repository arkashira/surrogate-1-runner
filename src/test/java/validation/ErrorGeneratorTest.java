package validation;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ErrorGeneratorTest {

    @Test
    public void testGenerateErrorMessage() {
        String collectionName = "MyCollection";
        String issueDetails = "ConcurrentModificationException detected";
        String expectedMessage = "Issue found in collection MyCollection: ConcurrentModificationException detected";
        String errorMessage = ErrorGenerator.generateErrorMessage(collectionName, issueDetails);
        assertEquals(expectedMessage, errorMessage);
    }

    @Test
    public void testGenerateErrorMessages() {
        Map<String, String> issues = new HashMap<>();
        issues.put("Collection1", "Issue1");
        issues.put("Collection2", "Issue2");

        List<String> expectedMessages = List.of(
                "Issue found in collection Collection1: Issue1",
                "Issue found in collection Collection2: Issue2"
        );

        List<String> errorMessages = ErrorGenerator.generateErrorMessages(issues);
        assertEquals(expectedMessages, errorMessages);
    }
}