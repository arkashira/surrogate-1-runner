package com.axentx.seo;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.http.*;
import javax.servlet.annotation.WebServlet;

/**
 * Simple SEO Dashboard servlet.
 * <p>
 * This servlet exposes a single endpoint `/seo-dashboard` that returns
 * key SEO metrics in JSON format. The metrics are currently hard‑coded
 * but can be replaced with real data sources in the future.
 * </p>
 */
@WebServlet(name = "SeoDashboardServlet", urlPatterns = {"/seo-dashboard"})
public class SeoDashboard extends HttpServlet {

    private static final long serialVersionUID = 1L;

    /**
     * Handles GET requests and returns a JSON payload with SEO metrics.
     */
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        // Set response type to JSON
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");

        // Dummy metrics – replace with real data sources
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("organicTraffic", 12345);
        metrics.put("keywordRanking", 8.7);
        metrics.put("backlinks", 256);
        metrics.put("crawlErrors", 3);
        metrics.put("pageSpeedScore", 92);

        // Convert map to JSON string
        String json = mapToJson(metrics);

        // Write response
        resp.getWriter().write(json);
    }

    /**
     * Very small JSON serializer for simple maps.
     * @param map Map to serialize
     * @return JSON string
     */
    private String mapToJson(Map<String, Object> map) {
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        boolean first = true;
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            if (!first) {
                sb.append(",");
            }
            sb.append("\"").append(entry.getKey()).append("\":");
            Object val = entry.getValue();
            if (val instanceof Number) {
                sb.append(val);
            } else {
                sb.append("\"").append(val).append("\"");
            }
            first = false;
        }
        sb.append("}");
        return sb.toString();
    }
}