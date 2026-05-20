package com.axentx.surrogate1;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Immutable representation of an upstream API request signature.
 * The list of parameters is stored sorted to make equality order‑independent.
 */
public final class Signature {
    private final String method;
    private final String path;
    private final List<String> params;   // sorted, unmodifiable

    @JsonCreator
    public Signature(
            @JsonProperty("method") String method,
            @JsonProperty("path") String path,
            @JsonProperty("params") List<String> params) {

        this.method = Objects.requireNonNull(method);
        this.path   = Objects.requireNonNull(path);
        // Defensive copy + sort → deterministic equality
        List<String> copy = params == null ? List.of() : List.copyOf(params);
        copy = copy.stream().sorted().toList();
        this.params = Collections.unmodifiableList(copy);
    }

    // Getters (Jackson needs them)
    public String method() { return method; }
    public String path()   { return path; }
    public List<String> params() { return params; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Signature that)) return false;
        return method.equals(that.method) &&
               path.equals(that.path) &&
               params.equals(that.params);
    }

    @Override
    public int hashCode() {
        return Objects.hash(method, path, params);
    }

    @Override
    public String toString() {
        return "Signature{" +
                "method='" + method + '\'' +
                ", path='" + path + '\'' +
                ", params=" + params +
                '}';
    }
}