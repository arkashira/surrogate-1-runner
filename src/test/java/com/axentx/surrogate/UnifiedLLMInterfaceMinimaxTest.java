package com.axentx.surrogate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

import com.axentx.surrogate.llm.MinimaxClient;
import com.axentx.surrogate.llm.UnifiedLLMInterface;
import com.axentx.surrogate.llm.UnifiedLLMRequest;
import com.axentx.surrogate.llm.UnifiedLLMResponse;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

/**
 * Test that the UnifiedLLMInterface correctly forwards a request to the Minimax provider
 * and returns the provider's response back to the caller.
 */
public class UnifiedLLMInterfaceMinimaxTest {

    @Mock
    private MinimaxClient minimaxClient;

    private UnifiedLLMInterface unifiedInterface;

    @BeforeEach
    public void setUp() {
        // Initialize mocks before each test method
        MockitoAnnotations.openMocks(this);
        // Inject the mocked Minimax client into the unified interface
        unifiedInterface = new UnifiedLLMInterface(minimaxClient);
    }

    @Test
    public void testMinimaxRequestForwarding() {
        // Arrange: Prepare the request and expected response
        String prompt = "Hello, Minimax!";
        UnifiedLLMRequest request = new UnifiedLLMRequest(prompt, "minimax");
        String expectedResponseText = "Hi there!";

        // Mock the Minimax client behavior
        UnifiedLLMResponse mockedResponse = new UnifiedLLMResponse(expectedResponseText);
        when(minimaxClient.sendRequest(request)).thenReturn(mockedResponse);

        // Act: Call the method under test
        UnifiedLLMResponse actualResponse = unifiedInterface.sendRequest(request);

        // Assert: Verify the response content
        assertEquals(expectedResponseText, actualResponse.getResponseText(),
                "The response text should match the Minimax provider's output");

        // Verify: Ensure the unified interface actually forwarded the request to the Minimax client
        verify(minimaxClient, times(1)).sendRequest(request);
    }
}