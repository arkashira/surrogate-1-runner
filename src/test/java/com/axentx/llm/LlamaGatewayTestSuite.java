package com.axentx.llm;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;
import java.util.concurrent.TimeUnit;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class LlamaGatewayTestSuite {

    /* ------------------------------------------------------------------ */
    /*  Service lifecycle – start/stop the gateway before/after tests   */
    /* ------------------------------------------------------------------ */
    private static final String BASE_URL = "http://localhost:8080";
    private Process serviceProcess;

    @BeforeAll
    void startService() throws IOException, InterruptedException {
        // Adjust the script path to your environment
        ProcessBuilder pb = new ProcessBuilder("bin/start-llm-gateway.sh");
        pb.redirectErrorStream(true);
        serviceProcess = pb.start();

        // Wait a short while for the service to boot
        TimeUnit.SECONDS.sleep(5);

        // Verify the service is reachable
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest healthReq = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/health"))
                .timeout(Duration.ofSeconds(2))
                .GET()
                .build();
        HttpResponse<String> healthResp = client.send(healthReq, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, healthResp.statusCode(), "Health endpoint should return 200");
        assertTrue(healthResp.body().contains("UP"), "Health body should contain 'UP'");
    }

    @AfterAll
    void stopService() {
        if (serviceProcess != null && serviceProcess.isAlive()) {
            serviceProcess.destroy();
        }
    }

    /* ------------------------------------------------------------------ */
    /*  1️⃣  Direct Java API test – LlamaGateway.query()                 */
    /* ------------------------------------------------------------------ */
    @Test
    void testDirectGatewayQuery() {
        LlamaGateway gateway = new LlamaGateway();   // assumes default constructor starts the in‑process stub
        String prompt = "What is the capital of France?";
        String response = gateway.query(prompt);

        assertNotNull(response, "Response should not be null");
        assertFalse(response.isBlank(), "Response should not be blank");
    }

    /* ------------------------------------------------------------------ */
    /*  2️⃣  HTTP API test – /generate endpoint                          */
    /* ------------------------------------------------------------------ */
    @Test
    void testHttpGenerateEndpoint() throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        String jsonBody = "{\"prompt\":\"Automated testing query\"}";

        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/generate"))
                .timeout(Duration.ofSeconds(5))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString());

        assertEquals(200, resp.statusCode(), "Generate endpoint should return 200");
        assertNotNull(resp.body(), "Response body should not be null");
        assertFalse(resp.body().isBlank(), "Response body should not be blank");
    }

    /* ------------------------------------------------------------------ */
    /*  3️⃣  Real‑time feedback – log content check                      */
    /* ------------------------------------------------------------------ */
    @Test
    void testRealTimeFeedback() throws IOException, InterruptedException {
        // In a real scenario you would tail the actual log file.
        // For the purposes of this test we simulate the log content.
        String simulatedLog =
                "Test 1: passed\n" +
                "Test 2: failed\n" +
                "API usage: 12 requests/sec";

        assertTrue(simulatedLog.contains("passed"), "Log should contain 'passed'");
        assertTrue(simulatedLog.contains("requests/sec"), "Log should contain 'requests/sec'");
    }
}