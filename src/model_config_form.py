import tkinter as tk
from tkinter import messagebox
from user_config import UserConfig

class ModelConfigForm:
    def __init__(self, root):
        self.root = root
        self.user_config = UserConfig()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Model Configuration")

        # Temperature
        tk.Label(self.root, text="Temperature (0-2):").grid(row=0, column=0, padx=10, pady=5)
        self.temperature_var = tk.DoubleVar(value=0.7)
        self.temperature_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, variable=self.temperature_var)
        self.temperature_slider.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.root, text="Controls randomness in output. Lower values make output more deterministic.").grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Top P
        tk.Label(self.root, text="Top P (0-1):").grid(row=2, column=0, padx=10, pady=5)
        self.top_p_var = tk.DoubleVar(value=0.9)
        self.top_p_entry = tk.Entry(self.root, textvariable=self.top_p_var)
        self.top_p_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.root, text="Controls diversity via nucleus sampling. Lower values make output more focused.").grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Max Tokens
        tk.Label(self.root, text="Max Tokens:").grid(row=4, column=0, padx=10, pady=5)
        self.max_tokens_var = tk.IntVar(value=100)
        self.max_tokens_entry = tk.Entry(self.root, textvariable=self.max_tokens_var)
        self.max_tokens_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Label(self.root, text="Maximum number of tokens to generate.").grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Save Button
        tk.Button(self.root, text="Save", command=self.save_config).grid(row=6, column=0, columnspan=2, pady=10)

    def save_config(self):
        temperature = self.temperature_var.get()
        top_p = float(self.top_p_var.get())
        max_tokens = self.max_tokens_var.get()

        if not self.user_config.validate_params(temperature, top_p, max_tokens):
            messagebox.showerror("Error", "Invalid parameters. Please check the ranges.")
            return

        self.user_config.set_model_params(temperature, top_p, max_tokens)
        messagebox.showinfo("Success", "Configuration saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModelConfigForm(root)
    root.mainloop()