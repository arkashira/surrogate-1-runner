package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;

import java.util.Date;

import static org.junit.jupiter.api.Assertions.*;

public class TaskListDashboardTest {

    @Test
    public void testAddAndDisplayTasks() {
        TaskListDashboard dashboard = new TaskListDashboard();
        dashboard.addTask("Task 1", new Date());
        dashboard.addTask("Task 2", new Date());

        dashboard.displayTasks();

        assertEquals(2, dashboard.tasks.size());
    }

    @Test
    public void testMarkTaskAsCompleted() {
        TaskListDashboard dashboard = new TaskListDashboard();
        dashboard.addTask("Task 1", new Date());
        dashboard.markTaskAsCompleted(0);

        assertFalse(dashboard.tasks.get(0).isCompleted());
    }
}