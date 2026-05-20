package com.axentx.surrogate1.orchestration;

import java.util.List;
import java.util.Objects;

public class Workflow {
    private String name;
    private List<Task> tasks;

    public Workflow() {}

    public Workflow(String name, List<Task> tasks) {
        this.name = name;
        this.tasks = tasks;
    }

    // Getters and Setters
    public String getName() { return name; }
    public List<Task> getTasks() { return tasks; }
    public void setName(String name) { this.name = name; }
    public void setTasks(List<Task> tasks) { this.tasks = tasks; }

    // Equals, HashCode, and ToString methods
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Workflow)) return false;
        Workflow workflow = (Workflow) o;
        return Objects.equals(name, workflow.name) &&
               Objects.equals(tasks, workflow.tasks);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, tasks);
    }

    @Override
    public String toString() {
        return "Workflow{" +
               "name='" + name + '\'' +
               ", tasks=" + tasks +
               '}';
    }
}

// Task.java
package com.axentx.surrogate1.orchestration;

import java.util.Map;
import java.util.Objects;

public class Task {
    private String id;
    private String type;
    private Map<String, Object> params;

    public Task() {}

    public Task(String id, String type, Map<String, Object> params) {
        this.id = id;
        this.type = type;
        this.params = params;
    }

    // Getters and Setters
    public String getId() { return id; }
    public String getType() { return type; }
    public Map<String, Object> getParams() { return params; }
    public void setId(String id) { this.id = id; }
    public void setType(String type) { this.type = type; }
    public void setParams(Map<String, Object> params) { this.params = params; }

    // Equals, HashCode, and ToString methods
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Task)) return false;
        Task task = (Task) o;
        return Objects.equals(id, task.id) &&
               Objects.equals(type, task.type) &&
               Objects.equals(params, task.params);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, type, params);
    }

    @Override
    public String toString() {
        return "Task{" +
               "id='" + id + '\'' +
               ", type='" + type + '\'' +
               ", params=" + params +
               '}';
    }
}