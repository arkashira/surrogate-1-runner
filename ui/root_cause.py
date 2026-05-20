import tkinter as tk
from tkinter import ttk

class RootCauseAnalysisUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AlertForge Root-Cause Analysis")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Frame for root cause display
        self.root_cause_frame = ttk.Frame(self, padding="10")
        self.root_cause_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Label for root cause title
        self.root_cause_title = ttk.Label(self.root_cause_frame, text="Root Cause Analysis", font=("Helvetica", 16))
        self.root_cause_title.grid(row=0, column=0, pady=10)

        # Text widget for displaying root cause details
        self.root_cause_text = tk.Text(self.root_cause_frame, wrap=tk.WORD, width=80, height=20)
        self.root_cause_text.grid(row=1, column=0, padx=10, pady=10)

        # Scrollbar for root cause text
        self.root_cause_scroll = ttk.Scrollbar(self.root_cause_frame, orient=tk.VERTICAL, command=self.root_cause_text.yview)
        self.root_cause_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.root_cause_text.configure(yscrollcommand=self.root_cause_scroll.set)

        # Frame for configuration options
        self.config_frame = ttk.Frame(self, padding="10")
        self.config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Label for configuration title
        self.config_title = ttk.Label(self.config_frame, text="Configuration Options", font=("Helvetica", 14))
        self.config_title.grid(row=0, column=0, pady=10)

        # Option menu for user preferences
        self.preference_var = tk.StringVar()
        self.preference_menu = ttk.OptionMenu(self.config_frame, self.preference_var, "Default", "Option 1", "Option 2", "Option 3")
        self.preference_menu.grid(row=1, column=0, padx=10, pady=10)

if __name__ == "__main__":
    app = RootCauseAnalysisUI()
    app.mainloop()