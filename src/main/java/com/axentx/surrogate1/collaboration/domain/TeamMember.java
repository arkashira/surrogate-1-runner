package com.axentx.surrogate1.collaboration.domain;

import java.util.Objects;

public final class TeamMember {
    private final String id;
    private final String name;
    private final String email;
    private final String role;

    public TeamMember(String id, String name, String email, String role) {
        this.id = Objects.requireNonNull(id);
        this.name = Objects.requireNonNull(name);
        this.email = Objects.requireNonNull(email);
        this.role = Objects.requireNonNull(role);
    }

    // getters …
}