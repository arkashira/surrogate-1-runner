import tkinter as tk
from tkinter import ttk
import paramiko
import threading

class InstanceSelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Instance Selection")

        self.instances = ["instance1", "instance2", "instance3"]  # Example instances
        self.selected_instance = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self.root, text="Select an instance:")
        label.pack(pady=10)

        dropdown = ttk.Combobox(self.root, textvariable=self.selected_instance)
        dropdown['values'] = self.instances
        dropdown.pack(pady=10)

        connect_button = ttk.Button(self.root, text="Connect", command=self.connect_to_instance)
        connect_button.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="Status: Ready")
        self.status_label.pack(pady=10)

    def connect_to_instance(self):
        instance = self.selected_instance.get()
        if not instance:
            self.status_label.config(text="Status: Please select an instance")
            return

        self.status_label.config(text=f"Status: Connecting to {instance}...")
        threading.Thread(target=self.ssh_connect, args=(instance,)).start()

    def ssh_connect(self, instance):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(instance, username='user', password='password')  # Replace with actual credentials
            self.root.after(0, lambda: self.status_label.config(text=f"Status: Connected to {instance}"))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"Status: Connection failed: {str(e)}"))
        finally:
            ssh.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = InstanceSelection(root)
    root.mainloop()