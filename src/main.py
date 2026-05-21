import threading
from thermal_monitor import ThermalMonitor

def start_thermal_monitor():
    monitor = ThermalMonitor()
    monitor_thread = threading.Thread(target=monitor.monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

if __name__ == "__main__":
    start_thermal_monitor()
    # Other main application code