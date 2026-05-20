import tkinter as tk
from tkinter import ttk
from terminal_environment import TerminalEnvironment

class CollaborationUI:
    def __init__(self, root, environment: TerminalEnvironment):
        self.root = root
        self.environment = environment
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Axentx Collaboration Terminal")
        self.root.geometry("800x600")

        self.terminal_frame = ttk.Frame(self.root, padding="10")
        self.terminal_frame.pack(fill="both", expand=True)

        self.terminal_text = tk.Text(
            self.terminal_frame, width=80, height=20, state="disabled"
        )
        self.terminal_text.pack(fill="both", expand=True)

        self.root.bind("<Key>", self.handle_key_press)

        self.update_terminal()

    def update_terminal(self):
        self.terminal_text.config(state="normal")
        self.terminal_text.delete("1.0", tk.END)
        self.terminal_text.insert(tk.END, self.environment.get_current_state())
        self.terminal_text.config(state="disabled")
        self.root.after(100, self.update_terminal)

    def handle_key_press(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.environment.move_cursor(event.keysym)
        elif event.keysym == "Return":
            self.environment.execute_command()
        else:
            self.environment.add_to_command(event.char)

        self.update_terminal()

# /opt/axentx/surrogate-1/src/terminal_environment.py

class TerminalEnvironment:
    def __init__(self):
        self.callbacks = set()
        self.command_history = []
        self.current_command_index = 0
        self.command = ""
        self.cursor_position = 0

    def register_callback(self, callback):
        self.callbacks.add(callback)

    def unregister_callback(self, callback):
        self.callbacks.discard(callback)

    def update(self, content):
        for callback in self.callbacks:
            callback(content)

    def get_current_state(self):
        return f"Command: {self.command}\nHistory: {self.command_history}\nCursor: {self.cursor_position}"

    def move_cursor(self, direction):
        if direction == "Left":
            self.cursor_position = max(0, self.cursor_position - 1)
        elif direction == "Right":
            self.cursor_position = min(len(self.command), self.cursor_position + 1)

    def add_to_command(self, char):
        self.command = self.command[:self.cursor_position] + char + self.command[self.cursor_position:]
        self.cursor_position += 1

    def execute_command(self):
        self.command_history.append(self.command)
        self.command = ""
        self.current_command_index = len(self.command_history)
        self.cursor_position = 0

    def get_command_history(self):
        return self.command_history

# /opt/axentx/surrogate-1/src/main.py
from ui import CollaborationUI
from terminal_environment import TerminalEnvironment

def main():
    root = tk.Tk()
    environment = TerminalEnvironment()
    ui = CollaborationUI(root, environment)
    root.mainloop()

if __name__ == "__main__":
    main()