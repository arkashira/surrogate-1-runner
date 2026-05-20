package com.axentx.surrogate;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * Unit tests for {@link LLMAgentApi}.
 *
 * These tests verify basic contract behavior:
 * <ul>
 *   <li>Calling the agent with a valid prompt returns a non‑null response.</li>
 *   <li>Calling the agent with a {@code null} or empty prompt throws
 *       {@link IllegalArgumentException}.</li>
 *   <li>The underlying HTTP client is invoked exactly once per call.</li>
 * </ul>
 *
 * The real {@code LLMAgentApi} depends on an {@code HttpClient} (or similar)
 * to communicate with the LLM service.  Mockito is used to stub that client
 * so the tests run fast and deterministically.
 */
class LLMAgentApiTest {

    private LLMAgentApi llmAgentApi;
    private HttpClient mockHttpClient;

    @BeforeEach
    void setUp() {
        // Create a mock HttpClient (the concrete type used by LLMAgentApi may differ;
        // replace with the actual class name if needed.)
        mockHttpClient = mock(HttpClient.class);
        // Inject the mock into the LLMAgentApi.  Assume a constructor that accepts the client.
        llmAgentApi = new LLMAgentApi(mockHttpClient);
    }

    @Test
    @DisplayName("callAgent returns a non‑null response for a valid prompt")
    void callAgentReturnsResponse() throws Exception {
        // Arrange
        String prompt = "Explain quantum entanglement in one sentence.";
        String expectedResponse = "Quantum entanglement is a physical phenomenon where particles become linked and instantaneously affect each other regardless of distance.";
        when(mockHttpClient.post(anyString(), eq(prompt))).thenReturn(expectedResponse);

        // Act
        String actual = llmAgentApi.callAgent(prompt);

        // Assert
        assertNotNull(actual, "Response should not be null");
        assertEquals(expectedResponse, actual, "Response should match the stubbed value");
        verify(mockHttpClient, times(1)).post(anyString(), eq(prompt));
    }

    @Test
    @DisplayName("callAgent throws IllegalArgumentException for null prompt")
    void callAgentRejectsNullPrompt() {
        assertThrows(IllegalArgumentException.class, () -> llmAgentApi.callAgent(null));
    }

    @Test
    @DisplayName("callAgent throws IllegalArgumentException for empty prompt")
    void callAgentRejectsEmptyPrompt() {
        assertThrows(IllegalArgumentException.class, () -> llmAgentApi.callAgent(""));
    }

    @Nested
    @DisplayName("Error handling")
    class ErrorHandling {

        @Test
        @DisplayName("propagates IOException from the HTTP client")
        void propagatesIOException() throws Exception {
            String prompt = "Test prompt";
            when(mockHttpClient.post(anyString(), eq(prompt))).thenThrow(new java.io.IOException("network error"));

            Exception ex = assertThrows(RuntimeException.class, () -> llmAgentApi.callAgent(prompt));
            assertTrue(ex.getCause() instanceof java.io.IOException);
            assertEquals("network error", ex.getCause().getMessage());
        }
    }
}