"""
Lightweight GUI for BatteryGuard.

This module provides a simple Tkinter window that displays historical
trend graphs for battery capacity and temperature. The graphs are
generated from CSV files located in the `data/` directory. The GUI
can be launched with the command:

    batteryguard gui

The command is wired in the package entry points (see setup.cfg).
"""

import os
import sys
import csv
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path

import matplotlib
# Use the TkAgg backend for Tkinter integration
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).parent.parent / "data"
CAPACITY_FILE = DATA_DIR / "capacity_history.csv"
TEMP_FILE = DATA_DIR / "temperature_history.csv"


def load_csv(file_path: Path):
    """Load a CSV file with columns: timestamp,value."""
    if not file_path.exists():
        return [], []
    times = []
    values = []
    with file_path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = datetime.fromisoformat(row["timestamp"])
                val = float(row["value"])
            except Exception:
                continue
            times.append(ts)
            values.append(val)
    return times, values


class BatteryGuardGUI(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("BatteryGuard - Historical Trends")
        self.geometry("800x600")
        self.resizable(False, False)

        # Create notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Capacity tab
        cap_frame = ttk.Frame(notebook)
        notebook.add(cap_frame, text="Capacity")
        self._create_graph(cap_frame, CAPACITY_FILE, "Capacity (%)")

        # Temperature tab
        temp_frame = ttk.Frame(notebook)
        notebook.add(temp_frame, text="Temperature")
        self._create_graph(temp_frame, TEMP_FILE, "Temperature (°C)")

        # Status bar
        status = ttk.Label(self, text="Data loaded", relief="sunken", anchor="w")
        status.pack(fill="x", side="bottom")

    def _create_graph(self, parent, file_path, ylabel):
        times, values = load_csv(file_path)
        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        if times and values:
            ax.plot(times, values, marker="o", linestyle="-")
            ax.set_xlabel("Time")
            ax.set_ylabel(ylabel)
            ax.grid(True)
            fig.autofmt_xdate()
        else:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def main():
    """Entry point for `batteryguard gui`."""
    app = BatteryGuardGUI()
    app.mainloop()


if __name__ == "__main__":
    main()