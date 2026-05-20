package main

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/urfave/cli/v2"
)

type Task struct {
	ID        int
	Title     string
	AssignedTo string
	Status    string
	DueDate   time.Time
}

var tasks = make([]Task, 0)

func main() {
	app := &cli.App{
		Commands: []*cli.Command{
			{
				Name:  "add",
				Usage: "Add a new task",
				Flags: []cli.Flag{
					&cli.IntFlag{Name: "id", Required: true},
					&cli.StringFlag{Name: "title", Required: true},
					&cli.StringFlag{Name: "assigned-to", Required: true},
					&cli.StringFlag{Name: "status", Value: "pending"},
					&cli.StringFlag{Name: "due-date", Required: true},
				},
				Action: func(c *cli.Context) error {
					id := c.Int("id")
					title := c.String("title")
					assignedTo := c.String("assigned-to")
					status := c.String("status")
					dueDate, _ := time.Parse("2006-01-02", c.String("due-date"))

					task := Task{ID: id, Title: title, AssignedTo: assignedTo, Status: status, DueDate: dueDate}
					tasks = append(tasks, task)
					fmt.Printf("Task %d added successfully\n", id)
					return nil
				},
			},
			{
				Name:  "list",
				Usage: "List all tasks",
				Action: func(c *cli.Context) error {
					for _, task := range tasks {
						fmt.Printf("ID: %d, Title: %s, Assigned To: %s, Status: %s, Due Date: %v\n", task.ID, task.Title, task.AssignedTo, task.Status, task.DueDate)
					}
					return nil
				},
			},
			{
				Name:  "complete",
				Usage: "Mark a task as complete",
				Flags: []cli.Flag{
					&cli.IntFlag{Name: "id", Required: true},
				},
				Action: func(c *cli.Context) error {
					id := c.Int("id")
					for i, task := range tasks {
						if task.ID == id {
							tasks[i].Status = "completed"
							fmt.Printf("Task %d marked as completed\n", id)
							return nil
						}
					}
					fmt.Printf("Task %d not found\n", id)
					return nil
				},
			},
		},
	}

	err := app.Run(os.Args)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}