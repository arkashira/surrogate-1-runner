package com.axentx.surrogate1;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class TaskListDashboard {
    private List<Task> tasks;

    public TaskListDashboard() {
        this.tasks = new ArrayList<>();
    }

    public void addTask(String description, Date dueDate) {
        Task task = new Task(description, dueDate);
        tasks.add(task);
    }

    public void markTaskAsCompleted(int taskId) {
        if (taskId >= 0 && taskId < tasks.size()) {
            tasks.get(taskId).setCompleted(true);
        }
    }

    public void displayTasks() {
        for (int i = 0; i < tasks.size(); i++) {
            Task task = tasks.get(i);
            System.out.println("Task ID: " + i);
            System.out.println("Description: " + task.getDescription());
            System.out.println("Due Date: " + task.getDueDate());
            System.out.println("Completed: " + task.isCompleted());
            System.out.println("--------------------");
        }
    }

    private static class Task {
        private String description;
        private Date dueDate;
        private boolean completed;

        public Task(String description, Date dueDate) {
            this.description = description;
            this.dueDate = dueDate;
            this.completed = false;
        }

        public String getDescription() {
            return description;
        }

        public Date getDueDate() {
            return dueDate;
        }

        public boolean isCompleted() {
            return completed;
        }

        public void setCompleted(boolean completed) {
            this.completed = completed;
        }
    }
}