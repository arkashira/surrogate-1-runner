package com.axentx.costradar;

import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Benchmarks {

    private static final String BENCHMARK_API_URL = "https://api.benchmark.best/components";

    public static JSONObject getRealTimeBenchmarks(double budget) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BENCHMARK_API_URL + "?budget=" + budget))
                .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return new JSONObject(response.body());
    }
}