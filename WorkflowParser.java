package com.axentx.surrogate1.orchestration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

public class WorkflowParser {

    private static final ObjectMapper JSON_MAPPER = new ObjectMapper();
    private static final ObjectMapper YAML_MAPPER = new ObjectMapper(new YAMLFactory());

    /**
     * Parses a workflow definition from a file. Supports JSON and YAML based on file extension.
     *
     * @param path Path to the workflow definition file.
     * @return Parsed Workflow object.
     * @throws IOException if file cannot be read or parsing fails.
     */
    public static Workflow parse(Path path) throws IOException {
        String fileName = path.getFileName().toString().toLowerCase();
        try (InputStream is = Files.newInputStream(path)) {
            if (fileName.endsWith(".json")) {
                return JSON_MAPPER.readValue(is, Workflow.class);
            } else if (fileName.endsWith(".yaml") || fileName.endsWith(".yml")) {
                return YAML_MAPPER.readValue(is, Workflow.class);
            } else {
                throw new IllegalArgumentException("Unsupported workflow file format: " + fileName);
            }
        }
    }
}