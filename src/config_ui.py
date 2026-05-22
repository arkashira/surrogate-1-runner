import tkinter as tk
from tkinter import ttk

class BotConfigUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Surrogate-1 DEX Protection Bot Configuration")

        # Create main frames
        self.config_frame = ttk.Frame(self.root)
        self.config_frame.pack(fill="both", expand=True)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill="x")

        # Create configuration widgets
        self.api_key_label = ttk.Label(self.config_frame, text="API Key:")
        self.api_key_label.pack(fill="x", padx=10, pady=5)

        self.api_key_entry = ttk.Entry(self.config_frame)
        self.api_key_entry.pack(fill="x", padx=10, pady=5)

        self.api_secret_label = ttk.Label(self.config_frame, text="API Secret:")
        self.api_secret_label.pack(fill="x", padx=10, pady=5)

        self.api_secret_entry = ttk.Entry(self.config_frame, show="*")
        self.api_secret_entry.pack(fill="x", padx=10, pady=5)

        # Create buttons
        self.save_button = ttk.Button(self.button_frame, text="Save Configuration", command=self.save_config)
        self.save_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.root.destroy)
        self.cancel_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    def save_config(self):
        api_key = self.api_key_entry.get()
        api_secret = self.api_secret_entry.get()

        # Save the configuration to a file or database here
        print(f"Saving config: API Key={api_key}, Secret Key={api_secret}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    config_ui = BotConfigUI(root)
    config_ui.run()