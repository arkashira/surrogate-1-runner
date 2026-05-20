package com.axentx.surrogate1;

import java.time.LocalDate;

public class Task {
    private String description;
    private LocalDate dueDate;
    private boolean completed;

    public Task(String description, LocalDate dueDate) {
        this.description = description;
        this.dueDate = dueDate;
        this.completed = false;
    }

    public String getDescription() {
        return description;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }
}
// src/main/java/com/axentx/surrogate1/TaskCompletionTracker.java
package com.axentx.surrogate1;

import java.util.ArrayList;
import java.util.List;

public class TaskCompletionTracker {
    private List<Task> tasks;

    public TaskCompletionTracker() {
        this.tasks = new ArrayList<>();
    }

    public void addTask(Task task) {
        tasks.add(task);
    }

    public void markTaskAsCompleted(int index) {
        if (index >= 0 && index < tasks.size()) {
            tasks.get(index).setCompleted(true);
        }
    }

    public List<Task> getTasks() {
        return tasks;
    }
}