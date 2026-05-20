import os
import json

class PRCreationTour:
    def __init__(self):
        self.steps = [
            {
                "title": "Step 1: Create a new PR",
                "description": "Click on the 'New PR' button to create a new pull request.",
                "action": "click",
                "target": "#new-pr-button"
            },
            {
                "title": "Step 2: Fill in the PR title and description",
                "description": "Enter a title and description for your PR.",
                "action": "fill",
                "target": "#pr-title, #pr-description"
            },
            {
                "title": "Step 3: Add files to the PR",
                "description": "Drag and drop files or click the 'Add files' button to add files to your PR.",
                "action": "drag-and-drop",
                "target": "#add-files-button"
            },
            {
                "title": "Step 4: Review and submit the PR",
                "description": "Review your PR and click the 'Submit' button to submit it.",
                "action": "click",
                "target": "#submit-button"
            }
        ]

    def start_tour(self):
        current_step = 0
        while current_step < len(self.steps):
            step = self.steps[current_step]
            print(f"Step {current_step + 1}: {step['title']}")
            print(step["description"])
            user_input = input("Do you want to (s)kip, (r)etry, or (c)ontinue? ")
            if user_input.lower() == "s":
                current_step += 1
            elif user_input.lower() == "r":
                current_step = 0
            elif user_input.lower() == "c":
                current_step += 1
            else:
                print("Invalid input. Please try again.")

    def skip_tour(self):
        print("Tour skipped.")

    def retry_tour(self):
        self.start_tour()

if __name__ == "__main__":
    tour = PRCreationTour()
    tour.start_tour()