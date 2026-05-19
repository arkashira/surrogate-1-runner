package com.axentx.surrogate1.orchestration;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Represents a node in an agent hierarchy.
 *
 * <p>Each node has a unique identifier, an optional parent, and a list of child nodes.
 * The class provides methods to add children, retrieve the hierarchy, and validate
 * that all required agents are defined before workflow launch.</p>
 */
public class AgentNode {

    private final String id;
    private final String name;
    private final String handler; // e.g., fully qualified class name or service identifier
    private AgentNode parent;
    private final List<AgentNode> children = new ArrayList<>();

    public AgentNode(String id, String name, String handler) {
        this.id = Objects.requireNonNull(id, "id must not be null");
        this.name = Objects.requireNonNull(name, "name must not be null");
        this.handler = Objects.requireNonNull(handler, "handler must not be null");
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getHandler() {
        return handler;
    }

    public AgentNode getParent() {
        return parent;
    }

    public List<AgentNode> getChildren() {
        return Collections.unmodifiableList(children);
    }

    /**
     * Adds a child node to this agent.
     *
     * @param child the child node to add
     * @throws IllegalArgumentException if the child is null or already has a parent
     */
    public void addChild(AgentNode child) {
        Objects.requireNonNull(child, "child must not be null");
        if (child.parent != null) {
            throw new IllegalArgumentException("Child already has a parent");
        }
        child.parent = this;
        children.add(child);
    }

    /**
     * Recursively validates that every node in the hierarchy has a non-null handler.
     *
     * @throws IllegalStateException if any node is missing a handler
     */
    public void validate() {
        if (handler == null || handler.isBlank()) {
            throw new IllegalStateException("AgentNode " + id + " has no handler defined");
        }
        for (AgentNode child : children) {
            child.validate();
        }
    }

    @Override
    public String toString() {
        return "AgentNode{id='" + id + "', name='" + name + "', handler='" + handler + "'}";
    }
}