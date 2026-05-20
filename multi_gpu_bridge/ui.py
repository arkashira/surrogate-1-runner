import tkinter as tk
from tkinter import ttk
import psutil

class MultiGPUBridgeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-GPU Bridge Configuration")
        
        # System Tray Icon
        self.tray_icon = None
        
        # GPU Selection Frame
        self.gpu_frame = ttk.Frame(self.root)
        self.gpu_frame.pack(padx=10, pady=10)
        
        self.gpu_label = ttk.Label(self.gpu_frame, text="Select GPUs:")
        self.gpu_label.pack()
        
        self.gpu_listbox = tk.Listbox(self.gpu_frame, selectmode=tk.MULTIPLE)
        self.gpu_listbox.pack()
        
        self.populate_gpu_list()
        
        # Performance Metrics Frame
        self.metrics_frame = ttk.Frame(self.root)
        self.metrics_frame.pack(padx=10, pady=10)
        
        self.metrics_label = ttk.Label(self.metrics_frame, text="Performance Metrics:")
        self.metrics_label.pack()
        
        self.metrics_text = tk.Text(self.metrics_frame, height=10, width=50)
        self.metrics_text.pack()
        
        self.update_metrics()
    
    def populate_gpu_list(self):
        gpus = psutil.sensors_temperatures().get('gpu_tegra', [])
        for gpu in gpus:
            self.gpu_listbox.insert(tk.END, gpu.label)
    
    def update_metrics(self):
        metrics = "GPU Usage:\n"
        for gpu in psutil.sensors_temperatures().get('gpu_tegra', []):
            metrics += f"{gpu.label}: {gpu.current}°C\n"
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(tk.END, metrics)
        
        self.root.after(1000, self.update_metrics)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiGPUBridgeUI(root)
    root.mainloop()