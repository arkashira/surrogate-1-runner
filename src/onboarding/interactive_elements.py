from typing import List, Dict

class InteractiveTourElement:
    def __init__(self, title: str, description: str, steps: List[Dict]):
        self.title = title
        self.description = description
        self.steps = steps
        self.current_step = 0

    def start_tour(self):
        print(f"Starting tour: {self.title}")
        self._show_current_step()

    def _show_current_step(self):
        step = self.steps[self.current_step]
        print(f"Step {self.current_step + 1}: {step['instruction']}")
        if 'example' in step:
            print(f"Example: {step['example']}")

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._show_current_step()
        else:
            print("End of tour reached.")

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._show_current_step()
        else:
            print("Already at the beginning of the tour.")

    def skip_tour(self):
        print("Tour skipped.")
        self.current_step = len(self.steps)

    def retry_tour(self):
        print("Retrying tour.")
        self.current_step = 0
        self.start_tour()


def create_tour(title: str, description: str, steps: List[Dict]) -> InteractiveTourElement:
    return InteractiveTourElement(title, description, steps)


# Example usage
if __name__ == "__main__":
    tour_steps = [
        {"instruction": "Welcome to Feature X", "example": "Try clicking here"},
        {"instruction": "Now let's explore Feature Y", "example": "See how it works"},
        {"instruction": "Finally, Feature Z", "example": "Complete the tour"}
    ]
    tour = create_tour("Core Features Tour", "Learn about our main functionalities", tour_steps)
    tour.start_tour()
    tour.next_step()
    tour.prev_step()
    tour.skip_tour()
    tour.retry_tour()