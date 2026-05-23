package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"time"
)

// Task represents a task to be assigned
type Task struct {
	ID        string
	Role      string
	CreatedAt time.Time
}

// User represents a user who can be assigned tasks
type User struct {
	ID       string
	Role     string
	Workload int
}

// Assignment represents an assignment of a task to a user
type Assignment struct {
	TaskID  string
	UserID  string
	AssignedAt time.Time
}

// Config represents the configuration for task assignment
type Config struct {
	RoleHierarchy map[string]int
}

var (
	config Config
	users  = make(map[string]User)
	tasks  = make(map[string]Task)
	assignments = make(map[string]Assignment)
	mu        sync.Mutex
)

func loadConfig() error {
	file, err := os.Open("config.yaml")
	if err != nil {
		return err
	}
	defer file.Close()

	var cfg Config
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&cfg)
	if err != nil {
		return err
	}

	config = cfg
	return nil
}

func addUser(user User) {
	mu.Lock()
	defer mu.Unlock()
	users[user.ID] = user
}

func addTask(task Task) {
	mu.Lock()
	defer mu.Unlock()
	tasks[task.ID] = task
}

func assignTask(taskID string) error {
	mu.Lock()
	defer mu.Unlock()

	task, exists := tasks[taskID]
	if !exists {
		return fmt.Errorf("task %s not found", taskID)
	}

	// Find the least busy user with the matching role
	var assignedUser *User
	for _, user := range users {
		if user.Role == task.Role {
			if assignedUser == nil || user.Workload < assignedUser.Workload {
				assignedUser = &user
			}
		}
	}

	if assignedUser == nil {
		return fmt.Errorf("no user found with role %s", task.Role)
	}

	// Create the assignment
	assignment := Assignment{
		TaskID:     taskID,
		UserID:     assignedUser.ID,
		AssignedAt: time.Now(),
	}
	assignments[taskID] = assignment

	// Update the user's workload
	assignedUser.Workload++

	return nil
}

func main() {
	// Load configuration
	err := loadConfig()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Example usage
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Add some users
	addUser(User{ID: "user1", Role: "developer", Workload: 0})
	addUser(User{ID: "user2", Role: "developer", Workload: 1})
	addUser(User{ID: "user3", Role: "designer", Workload: 0})

	// Add a task
	task := Task{ID: "task1", Role: "developer", CreatedAt: time.Now()}
	addTask(task)

	// Assign the task
	err = assignTask(task.ID)
	if err != nil {
		log.Fatalf("Failed to assign task: %v", err)
	}

	log.Println("Task assigned successfully")
}