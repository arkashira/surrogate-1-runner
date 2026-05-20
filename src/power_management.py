import time
import psutil
from gpu_monitor import GPUMonitor

class PowerManagement:
    def __init__(self):
        self.gpu_monitor = GPUMonitor()
        self.power_consumption_history = []
        self.temperature_history = []

    def monitor_power_consumption(self):
        while True:
            power_consumption = self.gpu_monitor.get_power_consumption()
            temperature = self.gpu_monitor.get_temperature()
            self.power_consumption_history.append(power_consumption)
            self.temperature_history.append(temperature)
            if len(self.power_consumption_history) > 10:
                self.power_consumption_history.pop(0)
                self.temperature_history.pop(0)
            time.sleep(5)

    def get_average_power_consumption(self):
        return sum(self.power_consumption_history) / len(self.power_consumption_history)

    def get_average_temperature(self):
        return sum(self.temperature_history) / len(self.temperature_history)

    def adjust_power_settings(self):
        average_power = self.get_average_power_consumption()
        average_temp = self.get_average_temperature()
        if average_power > 150 and average_temp > 80:
            self.gpu_monitor.reduce_power_consumption()
        elif average_power < 100 and average_temp < 70:
            self.gpu_monitor.increase_power_consumption()