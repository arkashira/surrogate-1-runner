
from tkinter import Tk, Frame, Label, Entry, Button, IntVar, StringVar

class Surrogate1Settings:
    def __init__(self, master):
        self.master = master
        self.master.title("Surrogate-1 Settings")

        self.settings_frame = Frame(self.master)
        self.settings_frame.pack(pady=20)

        self.max_workers_label = Label(self.settings_frame, text="Max Workers:")
        self.max_workers_label.grid(row=0, column=0)
        self.max_workers_entry = Entry(self.settings_frame)
        self.max_workers_entry.grid(row=0, column=1)

        self.max_workers = IntVar()
        self.max_workers.set(16)  # default value
        self.max_workers_entry.insert(0, str(self.max_workers.get()))

        self.save_button = Button(self.master, text="Save Settings", command=self.save_settings)
        self.save_button.pack(pady=20)

    def save_settings(self):
        max_workers = self.max_workers_entry.get()
        print(f"Saving Surrogate-1 settings: max_workers={max_workers}")
        # Save settings to a file or database here

root = Tk()
settings = Surrogate1Settings(root)
root.mainloop()